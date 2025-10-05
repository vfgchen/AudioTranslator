import os
import glob

from edge_srt_to_speech.__main__ import _main
import pysrt
import asyncio

def srt_to_speech(
        srt_dir = "subtitles",
        audio_dir = "audios",
        lang = "zh",
        voice = "zh-CN-XiaoxiaoNeural"):
    """
    srt_dir   : srt 输入目录
    audio_dir : audio 输出目录
    lang      : 配音语言
    voice     : 配音语音
    """

    # 创建 mp3 输出目录
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    for srt_file in glob.glob(os.path.join(srt_dir, f"**/*-{lang}.srt"), recursive=True):
        basename = os.path.basename(srt_file).split("-")[0]
        out_file = f"{audio_dir}/{basename}-{lang}.mp3"

        try:
            asyncio.get_event_loop().run_until_complete(_main(
                srt_data = pysrt.open(srt_file),
                voice = voice,
                out_file = out_file,
                rate = "+0%",
                volume = "+0%",
                batch_size = 50,
                enhanced_srt = False,
            ))
        finally:
            print(f"generate mp3: {out_file}")

if __name__ == "__main__":
    srt_to_speech(
        srt_dir="subtitles",
        audio_dir="audios",
        lang = "zh",
        voice="zh-CN-XiaoxiaoNeural"
    )