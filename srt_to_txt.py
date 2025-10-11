import os
from os import path
import glob
import argparse

import pysrt

# srt 修正，删除空行，无效行
def srt_correct(srt_file, ):
    # 读取 srt 文件
    subs = pysrt.open(srt_file)
    # 去除其中 text 为空的 sub
    filtered_subs = [sub for sub in subs if len(sub.text.strip()) > 1]
    # 去除短小的条目
    filtered_subs = [sub for sub in subs if not sub.text.strip(".,").lower() in ["yeah", "and", "or", "so"]]
    # 重新编号字幕索引
    for index, sub in enumerate(filtered_subs, start=1):
        sub.index = index
    # 重新保存srt
    pysrt.SubRipFile(items=filtered_subs).save(srt_file, encoding='utf-8')
    print(f"srt_correct: {srt_file}")
    return filtered_subs

# srt to txt
def srt_to_txt(
        srt_file,
        txt_file,
        is_correct_srt=False,
    ):
    # 创建 txt 文件的目录
    if not path.exists(path.dirname(txt_file)):
        os.makedirs(path.dirname(txt_file))
    # 读取并修正 srt_file
    if is_correct_srt:
        subs = srt_correct(srt_file)
    else:
        subs = pysrt.open(srt_file)
    # 有效文本保存到txt
    with open(txt_file, "w", encoding="utf-8") as txt:
        for sub in subs:
            txt.write(f"{sub.text}\n")
    print(f"srt_to_txt: {srt_file} -> {txt_file}")
    return txt_file

def srts_correct(
        srt_dir,
        suffix=".srt",
    ):
    for srt_file in glob.glob(path.join(srt_dir, f"**/*{suffix}"), recursive=True):
        srt_correct(srt_file)

def srts_to_txts(
        srt_dir,
        suffix="en.srt"
    ):
    for srt_file in glob.glob(path.join(srt_dir, f"**/*{suffix}"), recursive=True):
        txt_file = f"{path.splitext(srt_file)[0]}.txt"
        srt_to_txt(srt_file, txt_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="srt to txt")
    parser.add_argument("--func_name", help="func name", choices=["srts_correct", "srts_to_txts"], default="srts_to_txts")
    parser.add_argument("--srt_dir", help="srt dir", default="subtitles")
    parser.add_argument("--suffix", help="filename suffix", default="en.srt")
    args = parser.parse_args()

    func_name = args.func_name
    assert func_name in [
        "srts_correct",
        "srts_to_txts",
    ]

    globals()[func_name](
        srt_dir = args.srt_dir,
        suffix  = args.suffix,
    )
