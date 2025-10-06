## AudioTranslator

```
pip install ffmpeg
pip install whisper
pip install srtranslate
pip install srtranslator
pip install edge-srt-to-speech

# 或者安装最新稳定版（通常支持最新 CUDA）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

1. audio_converte.py
    对音频进行格式转换
2. audio_to_srt.py
    使用 openai-whisper 对音频进行语音识别，生成字幕
3. srt_translate.py
    对生成的字幕进行翻译成目标语言
4. srt_to_audio.py
    对翻译后的字幕进行语音合成生成目标语言的音频
5. audio_translate.py
    集合以上功能对音频进行翻译

* 支持批量操作
* 默认的音频文件路径 ./audios
* 默认的字幕文件路径 ./subtitles
* 需要预先安装 ffmpeg

  