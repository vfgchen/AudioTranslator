import os
import glob
import subprocess
import argparse

def video_to_navideo(
        in_video_file,
        na_video_file,
    ):
    """
    # 提取无声视频
        ffmpeg -y -i "demo-en.mp4" -an -vcodec copy "demo-na.mp4"
    """
    # 创建输出目录
    if not os.path.exists(os.path.dirname(na_video_file)):
        os.makedirs(os.path.dirname(na_video_file))
    # 提取视频流
    retcode = subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i",
            in_video_file,
            "-an",
            "-vcodec",
            "copy",
            na_video_file
        ],
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
    )
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, "ffmpeg")
    print(f"video_to_navideo: {na_video_file}")
    return na_video_file

def video_to_wav(
        in_video_file,
        wav_audio_file,
    ):
    """
    # 提取wav音频并以16khz输出, 语音识别需要wav文件
        ffmpeg -y -i "demo.mp4" -acodec pcm_s16le -ar 16000 "demo-en.wav"
    """
    # 创建输出目录
    if not os.path.exists(os.path.dirname(wav_audio_file)):
        os.makedirs(os.path.dirname(wav_audio_file))
    # 提取 16kHz WAV
    retcode = subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i",
            in_video_file,
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            wav_audio_file
        ],
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
    )
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, "ffmpeg")
    print(f"video_to_wav: {wav_audio_file}")
    return wav_audio_file

def video_to_mp3(
        in_video_file,
        mp3_audio_file,
    ):
    """
    # 提取 mp3 音频
        ffmpeg -y -i "demo.mp4" -acodec libmp3lame -ar 16000 "demo-en.mp3"
    """
    # 创建输出目录
    if not os.path.exists(os.path.dirname(mp3_audio_file)):
        os.makedirs(os.path.dirname(mp3_audio_file))
    # 提取 16kHz WAV
    retcode = subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i",
            in_video_file,
            "-acodec",
            "libmp3lame",
            "-ar",
            "16000",
            mp3_audio_file
        ],
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
    )
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, "ffmpeg")
    print(f"video_to_mp3: {mp3_audio_file}")
    return mp3_audio_file

def video_audio_srts_merge(
        in_video_file,
        in_audio_file,
        zh_srt_file,
        en_srt_file,
        out_video_file,
    ):
    """
    # 视频音频字幕合并
        ffmpeg -y
            -i "demo-na.mp4"
            -i "demo-zh.mp3"
            -i "demo-zh.srt"
            -i "demo-en.srt"
            -map 0 -dn -ignore_unknown -map -0:s
            -map 1 -dn -ignore_unknown -map -1:s
            -map 2:0 -metadata:s:s:0 "language=zho"
            -map 3:0 -metadata:s:s:1 "language=eng"
            -vcodec copy
            -acodec copy
            -strict experimental
            -c:s mov_text "output.mp4"
    """
    # 创建输出目录
    if not os.path.exists(os.path.dirname(out_video_file)):
        os.makedirs(os.path.dirname(out_video_file))
    # 视频音频字幕合并
    retcode = subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-i", in_video_file,
            "-i", in_audio_file,
            "-i", zh_srt_file,
            "-i", en_srt_file,
            "-map", "0", "-dn", "-ignore_unknown", "-map", "-0:s",
            "-map", "1", "-dn", "-ignore_unknown", "-map", "-1:s",
            "-map", "2:0", "-metadata:s:s:0", "language=zho",
            "-map", "3:0", "-metadata:s:s:1", "language=eng",
            "-vcodec", "copy",
            "-acodec", "copy",
            "-strict", "experimental",
            "-c:s", "mov_text",
            out_video_file
        ],
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
    )
    if retcode != 0:
        raise subprocess.CalledProcessError(retcode, "ffmpeg")
    print(f"video_audio_srts_merge: {out_video_file}")
    return out_video_file

def videos_to_navideos(
        video_dir,
        suffix=".mp4"
    ):
    for in_video_file in glob.glob(os.path.join(video_dir, f"**/*{suffix}"), recursive=True):
        basename = os.path.basename(in_video_file).split("-")[0]
        na_video_file = os.path.join(video_dir, f"{basename}-na.mp4")
        video_to_navideo(
            in_video_file=in_video_file,
            na_video_file=na_video_file,
        )

def videos_to_wavs(
        video_dir,
        suffix=".mp4"
    ):
    for in_video_file in glob.glob(os.path.join(video_dir, f"**/*{suffix}"), recursive=True):
        basename = os.path.basename(in_video_file).split("-")[0]
        wav_audio_file = os.path.join(video_dir, f"{basename}-en.wav")
        video_to_wav(
            in_video_file=in_video_file,
            wav_audio_file=wav_audio_file,
        )

def videos_to_mp3s(
        video_dir,
        suffix=".mp4"
    ):
    for in_video_file in glob.glob(os.path.join(video_dir, f"**/*{suffix}"), recursive=True):
        basename = os.path.basename(in_video_file).split("-")[0]
        mp3_audio_file = os.path.join(video_dir, f"{basename}-en.mp3")
        video_to_mp3(
            in_video_file=in_video_file,
            mp3_audio_file=mp3_audio_file,
        )

def videos_audios_srts_merge(
        video_dir,
        suffix="-zh.mp3"
    ):
    for zh_mp3_file in glob.glob(os.path.join(video_dir, f"**/*{suffix}"), recursive=True):
        basename = os.path.basename(zh_mp3_file).split("-")[0]
        na_video_file = os.path.join(video_dir, f"{basename}-na.mp4")
        zh_srt_file   = os.path.join(video_dir, f"{basename}-zh.srt")
        en_srt_file   = os.path.join(video_dir, f"{basename}-en.srt")
        zh_mp4_file   = os.path.join(video_dir, f"{basename}-zh.mp4")
        video_audio_srts_merge(
            in_video_file=na_video_file,
            in_audio_file=zh_mp3_file,
            zh_srt_file=zh_srt_file,
            en_srt_file=en_srt_file,
            out_video_file=zh_mp4_file,
        )

def videos_converte(
        command,
        video_dir="videos",
        suffix=".mp4",
    ):
    assert command in [
        "videos_to_navideos",
        "videos_to_wavs",
        "videos_to_mp3s",
        "videos_audios_srts_merge"
    ]
    return globals()[command](
        video_dir=video_dir,
        suffix=suffix
    )

if __name__ == "__main__":
    # videos_converte("videos_to_noaudio",        "D:/output", ".mp4")
    # videos_converte("videos_to_wavs",           "D:/output", ".mp4")
    # videos_converte("videos_to_mp3s",           "D:/output", ".mp4")
    # videos_converte("videos_audios_srts_merge", "D:/output", "zh.mp3")

    # --------------------------
    parser = argparse.ArgumentParser(description="videos converte")
    parser.add_argument("command", help="command", choices=[
        "videos_to_navideos",
        "videos_to_wavs",
        "videos_to_mp3s",
        "videos_audios_srts_merge"
    ])
    parser.add_argument("video_dir", help="video dir")
    parser.add_argument("suffix", help="file suffix")
    args = parser.parse_args()

    print(f"args: {args}")
    videos_converte(
        command = args.command,
        video_dir = args.video_dir,
        suffix = args.suffix
    )

    # ---------------------------
    # root_dir = "D:/output"
    # in_video_file  = os.path.join(root_dir, "104-en.mkv")
    # na_video_file  = os.path.join(root_dir, "104-na.mp4")
    # wav_audio_file = os.path.join(root_dir, "104-en.wav")
    # mp3_audio_file = os.path.join(root_dir, "104-en.mp3")

    # en_srt_file    = os.path.join(root_dir, "104-en.srt")
    # zh_srt_file    = os.path.join(root_dir, "104-zh.srt")
    # zh_mp3_file    = os.path.join(root_dir, "104-zh.mp3")
    # zh_video_file  = os.path.join(root_dir, "104-zh.mp4")

    # video_to_navideo(
    #     in_video_file=in_video_file,
    #     na_video_file=na_video_file
    # )

    # video_to_wav(
    #     in_video_file=in_video_file,
    #     wav_audio_file=wav_audio_file
    # )

    # video_to_mp3(
    #     in_video_file=in_video_file,
    #     mp3_audio_file=mp3_audio_file
    # )

    # video_audio_srts_merge(
    #     in_video_file=na_video_file,
    #     in_audio_file=zh_mp3_file,
    #     zh_srt_file=zh_srt_file,
    #     en_srt_file=en_srt_file,
    #     out_video_file=zh_video_file
    # )
