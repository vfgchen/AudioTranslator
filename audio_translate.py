import os
import glob

from audio_to_srt import audios_to_srts
from srt_translate import srts_translate
from srt_to_speech import srt_to_speech

def audio_translate(
        audio_dir = "audios",
        audio_type = "wav",
        from_lang = "en",
        to_lang = "zh",
        srt_dir = "subtitles",
        model_name = "base.en",
        model_dir = "./models",
    ):
    
    """
    audio_dir   : wav, mp3
    audio_type  : 默认 audios
    from_lang   : 默认 en
    to_lang     : 默认 zh
    model_name  : base.en, base, tiny.en, tiny
    model_dir   : 默认 ./models
    """

    # 创建 srt 目录
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)

    # 遍历 audio 进行语音识别，字幕翻译，语音合成
    for in_audio_file in glob.glob(os.path.join(audio_dir, f"**/*-{from_lang}.{audio_type}"), recursive=True):
        basename = os.path.basename(in_audio_file).split("-")[0]
        
        # 语音识别生成字幕
        from_lang_srt_file = os.path.join(srt_dir, f"{basename}-{from_lang}.srt")
        audios_to_srts(
            audio_dir=audio_dir,
            srt_dir=srt_dir,
            audio_type=audio_type,
            lang=from_lang,
            model_name=model_name,
            model_dir=model_dir,
        )

        #

if __name__ == "__main__":
    audio_translate(
        audio_dir="audios",
        audio_type="wav",
        from_lang="en",
        to_lang="zh",
        srt_dir="subtitles",
        model_name="base.en",
        model_dir="./models"
    )
