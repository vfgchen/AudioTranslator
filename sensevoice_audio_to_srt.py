import os
import io

import emoji
import soundfile
import torch
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

# 定义时间戳格式
def seconds_to_srttime(seconds):
    h, m  = divmod(seconds, 3600)
    m, s  = divmod(m, 60)
    s, ms = divmod(s, 1)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(ms * 1000):03d}"

# 音频转字幕
def audio_to_srt(wav_path, srt_path, vad_model, asr_model):
    # 获取 vad 分段
    vad_res = vad_model.generate(input=wav_path, cache={})
    vad_segments = vad_res[0]["value"]

    if len(vad_segments) <= 0: return srt_path

    # 创建 srt 文件目录
    if not os.path.exists(os.path.dirname(srt_path)):
        os.makedirs(os.path.dirname(srt_path))

    # 加载原始音频数据
    audio_data, sample_rate = soundfile.read(wav_path)

    # 对每个分段语音识别生成字幕
    srt_items = []
    for vad_segment in vad_segments:
        # 截取音频片段
        start, end = vad_segment  # 获取开始和结束时间
        start_sample = int(start * sample_rate / 1000)  # 转换为样本数
        end_sample = int(end * sample_rate / 1000)  # 转换为样本数
        audio_segment = audio_data[start_sample:end_sample]

        # 语音转文字处理
        with io.BytesIO() as buffer:
            soundfile.write(buffer, audio_segment, sample_rate, format="WAV")
            buffer.seek(0)  # 重置缓冲区指针到开头
            asr_res = asr_model.generate(input=buffer, cache={})

        # 处理输出结果
        text = rich_transcription_postprocess(asr_res[0]["text"])
        text = emoji.replace_emoji(text, replace="")  # 去除表情符号
        srt_items.append(f"{len(srt_items)+1}\n{seconds_to_srttime(start / 1000)} --> {seconds_to_srttime(end / 1000)}\n{text}\n\n")

    # 字幕写入到文件
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        for srt_item in srt_items:
            srt_file.write(srt_item)
    print(f"audio_to_srt: {srt_file}")
    return srt_file

if __name__ == "__main__":

    # 模型路径
    vad_model_dir = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
    vad_model_path = os.path.join("./models", vad_model_dir)

    asr_model_dir = "iic/SenseVoiceSmall"
    asr_model_path = os.path.join("./models", asr_model_dir)

    wav_path = "./audios/001-en.wav"
    srt_path = "./subtitles/001-en.srt"
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    lang = "en"

    # 加载VAD模型
    vad_model = AutoModel(
        model=vad_model_dir,
        model_path=vad_model_path,
        device=device,
        disable_update=True,
        max_single_segment_time=20000,  # 最大单个片段时长
        merge_length_s=15,  # 合并长度，单位为秒
        max_end_silence_time=500,  # 静音阈值，范围500ms～6000ms，默认值800ms。
    )

    # 加载SenseVoice模型
    asr_model = AutoModel(
        model=asr_model_dir,
        model_path=asr_model_path,
        device=device,
        disable_update=True,
        language=lang,
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  # 启用 VAD 断句
        ban_emo_unk=True,  # 禁用情感标签
    )

    # 模型推理生成字幕
    audio_to_srt(wav_path, srt_path, vad_model, asr_model)
