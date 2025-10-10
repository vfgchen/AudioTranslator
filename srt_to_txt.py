import os
from os import path
import glob
import argparse

import pysrt

# srt to txt
def srt_to_txt(
        srt_file,
        txt_file
    ):
    # 创建 txt 文件的目录
    if not path.exists(path.dirname(txt_file)):
        os.makedirs(path.dirname(txt_file))
    # 读取 srt 文件
    srt_data = pysrt.open(srt_file)
    # 去除其中 text 为空的 sub
    filtered_srt_data = [sub for sub in srt_data if len(sub.text.strip()) > 1]
    # 重新编号字幕索引
    for index, sub in enumerate(filtered_srt_data, start=1):
        sub.index = index
    # 重新保存srt
    pysrt.SubRipFile(items=filtered_srt_data).save(srt_file, encoding='utf-8')
    # 有效文本保存到txt
    with open(txt_file, "w") as txt:
        for sub in filtered_srt_data:
            txt.write(f"{sub.text}\n")

# txt to srt
def txt_to_srt(
        txt_file,
        srt_file,
        ref_srt_file,
    ):
    # 创建 srt_file 所在目录
    if not path.exists(path.dirname(srt_file)):
        os.makedirs(path.dirname(srt_file))
    # txt 行
    with open(txt_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if len(line.strip()) > 0]
    # ref_srt_file 行
    ref_subs = pysrt.open(ref_srt_file)
    for index, ref_sub in enumerate(ref_subs, start=1):
        ref_sub.index = index
        ref_sub.text = lines[index - 1]
    # 创建字幕文件
    srt_subs = pysrt.SubRipFile(ref_subs)
    srt_subs.save(srt_file, encoding="utf-8")


if __name__ == "__main__":
    # srt_file="D:/output/001-en.srt"
    # txt_file="D:/output/001-en.txt"
    # srt_to_txt(srt_file, txt_file)

    txt_file="D:/output/001-zh.txt"
    srt_file="D:/output/001-zh.srt"
    ref_srt_file="D:/output/001-en.srt"
    txt_to_srt(txt_file, srt_file, ref_srt_file)
