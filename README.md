## AudioTranslator

1. audio_to_srt.py
    使用 openai-whisper 对音频进行语音识别，生成字幕
2. srt_translate.py
    对生成的字幕进行翻译成目标语言
3. srt_to_audio.py
    对翻译后的字幕进行语言合成生成目标语言的音频
4. audio_translate.py
    集合以上功能对音频进行翻译

* 支持批量操作
* 默认的音频文件路径 ./audios
* 默认的字幕文件路径 ./subtitles
* 需要预先安装 ffmpeg
  pip install ffmpeg
  