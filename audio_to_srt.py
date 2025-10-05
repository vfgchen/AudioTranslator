import os
import glob
import whisper
import argparse

def seconds_to_time(total_seconds):
    """
    将总秒数转换为[HH:MM:,sss]格式
    :return: 格式化字符串，如 "02:35:17,123"
    """
    try:
        total_seconds = float(total_seconds)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int(total_seconds % 1 * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    except (ValueError, TypeError):
        return "无效输入"

def segments_to_srt(segments, srt_file):
    with open(srt_file, "w") as file:
        seq = 0
        for segment in segments["segments"]:
            seq = seq + 1
            start = seconds_to_time(segment["start"])
            end   = seconds_to_time(segment["end"])
            text  = segment["text"].strip()
            file.write(f"{seq}\n{start} --> {end}\n{text}\n\n")
    return srt_file

def audio_to_srt(
        audio_file,
        srt_file,
        model_name="base.en",
        model_dir="./models"
    ):
    # 创建 srt 目录
    srt_dir = os.path.dirname(srt_file)
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)
    # 使用模型
    model = whisper.load_model(
        name = model_name,
        download_root = model_dir)
    # 语言识别
    segments = model.transcribe(audio = audio_file, verbose = True)
    # 字幕保存到文件
    segments_to_srt(segments, srt_file)
    print(f"audio_to_srt: {srt_file}")
    return srt_file

def audios_to_srts(
    audio_dir   = "audios",
    srt_dir     = "subtitles",
    audio_type  = "wav",
    lang        = "en",
    model_name  = "base.en",
    model_dir   = "./models"
    ):
    """
    audio_dir   : wav, mp3
    srt_dir     : 默认 subtitles
    audio_type  : 默认 audios
    lang        : en, zh
    model_name  : base.en, base, tiny.en, tiny
    model_dir   : 默认./models
    """
    # 创建 srt 输出目录
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)
    # 遍历 wav 或 mp3 文件，生成 srt
    for audio_file in glob.glob(os.path.join(audio_dir, f"**/*-{lang}.{audio_type}"), recursive=True):
        basename = os.path.basename(audio_file).split("-")[0]
        srt_file = f"{srt_dir}/{basename}-{lang}.srt"
        audio_to_srt(
            audio_file=audio_file,
            srt_file=srt_file,
            model_name=model_name,
            model_dir=model_dir,
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("audio_dir", help="audio dir", default="audios")
    parser.add_argument("--srt_dir", help="srt dir", default="subtitles")
    parser.add_argument("--audio_type", help="audio type", default="mp3")
    parser.add_argument("--lang", help="lang", default="en")
    args = parser.parse_args()

    audios_to_srts(
        audio_dir   = args.audio_dir,
        srt_dir     = args.srt_dir,
        audio_type  = args.audio_type,
        lang        = args.lang,
    )
