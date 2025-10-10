import os
from os import path
import glob
import argparse

import pysrt

# srt 修正，删除空行，无效行
def srt_correct(srt_file):
    # 读取 srt 文件
    subs = pysrt.open(srt_file)
    # 去除其中 text 为空的 sub
    filtered_subs = [sub for sub in subs if len(sub.text.strip()) > 1]
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
    print(f"txt_to_srt: {txt_file} -> {srt_file}")
    return srt_file

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

def txts_to_srts(
        txt_dir,
        suffix="zh.txt",
        ref_srt_lang="en"
    ):
    for txt_file in glob.glob(path.join(txt_dir, f"**/*{suffix}"), recursive=True):
        basename = path.basename(txt_file).split("-")[0]
        srt_file = f"{path.splitext(txt_file)[0]}.srt"
        ref_srt_file = path.join(txt_dir, f"{basename}-{ref_srt_lang}.srt")
        print(ref_srt_file)
        assert path.exists(ref_srt_file)
        txt_to_srt(
            txt_file=txt_file,
            srt_file=srt_file,
            ref_srt_file=ref_srt_file
        )

if __name__ == "__main__":
    #-------------------
    # root_dir = "E:/Download/D365FO_Training/Udemy_PL200_Microsoft Power Platform Functional Consultant 2025-5"
    # en_srt_dir = path.join(root_dir, "en-srt")
    # srts_correct(en_srt_dir)
    # srts_to_txts(en_srt_dir)
    
    #-------------------
    srt_file="D:/output/001-en.srt"
    txt_file="D:/output/001-en.txt"
    srt_to_txt(srt_file, txt_file)

    #-------------------
    # txt_file="D:/output/001-zh.txt"
    # srt_file="D:/output/001-zh.srt"
    # ref_srt_file="D:/output/001-en.srt"
    # txt_to_srt(txt_file, srt_file, ref_srt_file)

    #-------------------
    # srt_dir="D:/output"
    # srts_correct(srt_dir)

    #-------------------
    # txt_dir="D:/output"
    # srts_to_txts(txt_dir)

    #-------------------
    # txt_dir="D:/output"
    # txts_to_srts(txt_dir)