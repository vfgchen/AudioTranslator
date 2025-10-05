import os
import glob
import argparse

from audio_to_srt import audio_to_srt
from srt_translate import srt_translate
from srt_to_audio import srt_to_audio

def audio_translate(
        in_audio_file,
        out_audio_file,
        from_lang="en",
        to_lang="zh",
        srt_dir="subtitles",
        voice="zh-CN-XiaoxiaoNeural",
        model_name="base.en",
        model_dir="./models",
    ):
    # 创建 srt 目录
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)
    # 中间文件基本名称
    basename = os.path.basename(in_audio_file).split("-")[0]
    # 语音识别生成 from_lang 字幕
    from_lang_srt_file = os.path.join(srt_dir, f"{basename}-{from_lang}.srt")
    audio_to_srt(
        audio_file=in_audio_file,
        srt_file=from_lang_srt_file,
        model_name=model_name,
        model_dir=model_dir
    )
    # from_lang 字幕翻译成 to_lang 字幕
    to_lang_srt_file = os.path.join(srt_dir, f"{basename}-{to_lang}.srt")
    srt_translate(
        in_srt_file=from_lang_srt_file,
        out_srt_file=to_lang_srt_file,
        from_lang=from_lang,
        to_lang=to_lang
    )
    # 创建 out_audio_file 所在的目录
    out_audio_dir = os.path.dirname(out_audio_file)
    if not os.path.exists(out_audio_dir):
        os.makedirs(out_audio_dir)
    # to_lang 字幕合成语音
    srt_to_audio(
        srt_file=to_lang_srt_file,
        audio_file=out_audio_file,
        voice=voice
    )
    print(f"audio_translate: {out_audio_file}")
    return out_audio_file

def audios_translate(
        audio_dir = "audios",
        audio_type = "wav",
        from_lang = "en",
        to_lang = "zh",
        srt_dir = "subtitles",
        voice="zh-CN-XiaoxiaoNeural",
        model_name = "base.en",
        model_dir = "./models",
    ):
    
    """
    # 批量音频翻译
    audio_dir   : 默认 audios
    audio_type  : 默认 wav
    from_lang   : 默认 en
    to_lang     : 默认 zh
    voice       : 默认 zh-CN-XiaoxiaoNeural
    model_name  : base.en, base, tiny.en, tiny
    model_dir   : 默认 ./models
    """
    # 创建 srt 目录
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)
    # 遍历 audio 进行语音识别，字幕翻译，语音合成
    for in_audio_file in glob.glob(os.path.join(audio_dir, f"**/*-{from_lang}.{audio_type}"), recursive=True):
        basename = os.path.basename(in_audio_file).split("-")[0]
        out_audio_file = os.path.join(audio_dir, f"{basename}-{to_lang}.mp3")
        audio_translate(
            in_audio_file=in_audio_file,
            out_audio_file=out_audio_file,
            from_lang=from_lang,
            to_lang=to_lang,
            srt_dir=srt_dir,
            voice=voice,
            model_name=model_name,
            model_dir=model_dir,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("audio_dir", help="audio dir", default="audios")
    parser.add_argument("--audio_type", help="audio type", default="wav")
    parser.add_argument("--from_lang", help="from lang", default="en")
    parser.add_argument("--to_lang", help="to lang", default="zh")
    parser.add_argument("--srt_dir", help="srt dir", default="subtitles")
    parser.add_argument("--model_name", help="model name", default="base.en")
    parser.add_argument("--model_dir", help="model dir", default="./models")
    args = parser.parse_args()

    audios_translate(
        audio_dir   = args.audio_dir,
        audio_type  = args.audio_type,
        from_lang   = args.from_lang,
        to_lang     = args.to_lang,
        srt_dir     = args.srt_dir,
        model_name  = args.model_name,
        model_dir   = args.model_dir,
    )
