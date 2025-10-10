import os
from os import path
import glob
import pysrt
import argparse

def check_aitxt(
        aitxt_file,
    ):
    lines = []
    # 读取文件行数
    with open(aitxt_file, "r", encoding="utf-8") as file:
        lines = [line for line in file if len(line.strip()) > 0]

    # 读取参考文件的行数
    basename = f"{path.splitext(aitxt_file)[0]}"
    ref_lines = []
    ref_file = f"{basename}.txt"
    print(ref_file)
    if path.exists(ref_file):
        with open(ref_file, "r", encoding="utf-8") as file:
            ref_lines = [line.strip() for line in file if len(line.strip()) > 0]
    else:
        ref_file = f"{basename}.srt"
        subs = pysrt.open(ref_file)
        ref_lines = [sub for sub in subs if len(sub.text.strip()) > 0]
    
    # 比对两者的行数
    return len(lines) == len(ref_lines)

def check_aitxts(
        aitxt_dir="subtitles",
        suffix="en.aitxt",
    ):
    result = []
    for aitxt_file in glob.glob(path.join(aitxt_dir, f"**/*{suffix}"), recursive=True):
        if not check_aitxt(aitxt_file=aitxt_file):
            result.append(aitxt_file)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--aitxt_dir", help="aitxt dir", default="subtitles")
    parser.add_argument("--suffix", help="filename suffix", default="en.aitxt")
    args = parser.parse_args()

    result = check_aitxts(
        aitxt_dir   = args.aitxt_dir,
        suffix      = args.suffix,
        )
    filenames = "\n".join([item for item in result])
    print(filenames)
    diff_file = path.join(args.aitxt_dir, "diff.txt")
    with open(diff_file, "w", encoding="utf-8") as file:
        file.write(filenames)
