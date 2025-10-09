import os
import glob
import subprocess
import argparse

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
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
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
    parser = argparse.ArgumentParser(description="audio format converte")
    parser.add_argument("audio_dir", help="audio dir", default="audios")
    parser.add_argument("--lang", help="audio lang", default="en")
    parser.add_argument("-f", help="from audio type", default="mp3")
    parser.add_argument("-t", help="to   audio type", default="wav")
    args = parser.parse_args()

    audio_dir = args.audio_dir
    lang      = args.lang
    from_type = args.f
    to_type   = args.t

    audios_converte(
        audio_dir       = audio_dir,
        lang            = lang,
        from_audio_type = from_type,
        to_audio_type   = to_type
    )