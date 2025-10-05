import os
import glob
import subprocess

def audio_converte(
        in_audio_file,
        out_audio_file,
    ):
    """
    音频格式转换: ffmpeg -y -i in_audio_file out_audio_file
    in_audio_file: 输入音频文件
    out_audio_file: 输出音频文件
    return: out_audio_file 输出音频文件
    """
    # 输出文件路径
    if in_audio_file == out_audio_file:
        return out_audio_file
    # ffmpeg -y -i in_audio_file out_audio_file
    retcode = subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i",
            in_audio_file,
            out_audio_file
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, "ffmpeg")
    print(f"audio_converte: {out_audio_file}")
    return out_audio_file

def audios_converte(
        audio_dir       = "audios",
        lang            = "en",
        from_audio_type = "mp3",
        to_audio_type   = "wav"
    ):
    for in_audio_file in glob.glob(os.path.join(audio_dir, f"**/*-{lang}.{from_audio_type}"), recursive=True):
        basename = os.path.basename(in_audio_file).split("-")[0]
        out_audio_file = os.path.join(audio_dir, f"{basename}-{lang}.{to_audio_type}")
        audio_converte(
            in_audio_file=in_audio_file,
            out_audio_file=out_audio_file
        )

if __name__ == "__main__":
    audios_converte()