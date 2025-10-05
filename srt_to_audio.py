import os
import glob

from edge_srt_to_speech.__main__ import _main
import pysrt
import asyncio

def srt_to_audio(
        srt_file,
        audio_file,
        voice="zh-CN-XiaoxiaoNeural"
    ):
    """
    srt_file   : srt 输入文件
    audio_file : audio 输出文件
    voice      : 配音语音
    """
    # 创建 audio 输出目录
    audio_dir = os.path.dirname(audio_file)
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    # 字幕语音合成
    asyncio.get_event_loop().run_until_complete(_main(
        srt_data = pysrt.open(srt_file),
        voice = voice,
        out_file = audio_file,
        rate = "+0%",
        volume = "+0%",
        batch_size = 50,
        enhanced_srt = False,
    ))
    print(f"srt_to_audio: {audio_file}")
    # 返回语音文件
    return audio_file

def srts_to_audios(
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

    # 创建 audio 输出目录
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    # 遍历 lang 语言字幕，合成语音
    for srt_file in glob.glob(os.path.join(srt_dir, f"**/*-{lang}.srt"), recursive=True):
        basename = os.path.basename(srt_file).split("-")[0]
        audio_file = f"{audio_dir}/{basename}-{lang}.mp3"
        # 合成语音
        srt_to_audio(
            srt_file=srt_file,
            audio_file=audio_file,
            voice=voice
        )

if __name__ == "__main__":
    srts_to_audios(
        srt_dir="subtitles",
        audio_dir="audios",
        lang = "zh",
        voice="zh-CN-XiaoxiaoNeural"
    )