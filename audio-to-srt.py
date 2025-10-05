import whisper

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
    model_name = "base.en",
    model_directory = "./models",
    wav_dir = "audios",
    out_dir = "subtitles"
    ):
    """
    model_name: whisper 语言识别模型
    model_directory: 模型下载目录
    """
    
    # 使用模型
    model = whisper.load_model(
        name = model_name,
        download_root = model_directory)

    segments = model.transcribe(
        audio = "demo-en.mp3",
        verbose = False,
        )
    
    segments_to_srt(segments, "demo-en.srt")

if __name__ == "__main__":
    audio_to_srt()
