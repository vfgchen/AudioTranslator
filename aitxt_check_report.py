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
    if path.exists(ref_file):
        with open(ref_file, "r", encoding="utf-8") as file:
            ref_lines = [line.strip() for line in file if len(line.strip()) > 0]
    else:
        ref_file = f"{basename}.srt"
        subs = pysrt.open(ref_file)
        ref_lines = [sub for sub in subs if len(sub.text.strip()) > 0]
    
    # 比对两者的行数
    is_match = len(lines) == len(ref_lines)
    report = f"txt: {aitxt_file}, ref: {ref_file}, txt_len: {len(lines)}, ref_len: {len(ref_lines)}"
    return is_match, report

def check_aitxts(
        aitxt_dir="subtitles",
        suffix="en.aitxt",
    ):
    result = []
    for aitxt_file in glob.glob(path.join(aitxt_dir, f"**/*{suffix}"), recursive=True):
        is_match, report = check_aitxt(aitxt_file=aitxt_file)
        if not is_match:
            result.append(report)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--aitxt_dir", help="aitxt dir", default="subtitles")
    parser.add_argument("--suffix", help="filename suffix", default="en.aitxt")
    parser.add_argument("--report_file", help="report diff file", default="report.diff")
    args = parser.parse_args()

    result = check_aitxts(
        aitxt_dir   = args.aitxt_dir,
        suffix      = args.suffix,
        )
    reports = "\n".join([item for item in result])
    print(reports)
    diff_file = path.join(args.aitxt_dir, args.report_file)
    with open(diff_file, "w", encoding="utf-8") as file:
        file.write(reports)
