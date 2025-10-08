## AudioTranslator

```
# whipser 模型
pip install ffmpeg
pip install openai-whisper
pip install srtranslator
pip install edge-srt-to-speech

# SenseVoice 模型
pip install funasr
pip install modelscope
pip install torch
pip install torchaudio
pip install emoji

# 下载SenseVoice模型
modelscope download --model iic/SenseVoiceSmall --local_dir models/iic/SenseVoiceSmall
modelscope download --model iic/speech_fsmn_vad_zh-cn-16k-common-pytorch --local_dir models/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch

```

1. audio_converte.py
    对音频进行格式转换
2. whisper_audio_to_srt.py
    使用 openai-whisper 对音频进行语音识别，生成字幕
3. sensevoice_audio_to_srt.py
    使用 SenseVoiceSmall 对音频进行语音识别，生成字幕
4. srt_translate.py
    对生成的字幕进行翻译成目标语言
5. srt_to_audio.py
    对翻译后的字幕进行语音合成生成目标语言的音频
6. audio_translate.py
    集合以上功能对音频进行翻译

* 支持批量操作
* 默认的音频文件路径 ./audios
* 默认的字幕文件路径 ./subtitles
* 需要预先安装 ffmpeg

  