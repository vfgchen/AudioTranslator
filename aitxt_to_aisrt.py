import os
from os import path
import glob
import argparse

import pysrt

# aitxt to aisrt
def aitxt_to_aisrt(
        aitxt_file,
        aisrt_file,
        ref_srt_lang="en",
    ):
    # 创建 aisrt_file 所在的目录
    if not path.exists(path.dirname(aisrt_file)):
        os.makedirs(path.dirname(aisrt_file))
    # aitxt 行
    with open(aitxt_file, 'r', encoding="utf-8") as file:
        ai_lines = file.readlines()
        ai_lines = [line.strip() for line in ai_lines if len(line.strip()) > 0]
    # ref_srt_file 行
    aitxt_dir = path.dirname(aitxt_file)
    basename = path.basename(aitxt_file).split("-")[0]
    ref_srt_file = path.join(aitxt_dir, f"{basename}-{ref_srt_lang}.srt")
    assert path.exists(ref_srt_file)
    ref_subs = pysrt.open(ref_srt_file)
    for index, ref_sub in enumerate(ref_subs, start=1):
        ref_sub.index = index
        ref_sub.text = ai_lines[index - 1]
        print(f"{index:03d} [{ref_sub.start} --> {ref_sub.end}] {ref_sub.text}")
    # 创建字幕文件
    srt_subs = pysrt.SubRipFile(ref_subs)
    srt_subs.save(aisrt_file, encoding="utf-8")
    print(f"aitxt_to_aisrt: {aitxt_file} -> {aisrt_file}")
    return aisrt_file

# aitxt 批量转 aisrt
def aitxts_to_aisrts(
        aitxt_dir,
        suffix=".aitxt",
        ref_srt_lang="en",
    ):
    for aitxt_file in glob.glob(path.join(aitxt_dir, f"**/*{suffix}"), recursive=True):
        basename = path.basename(aitxt_file).split("-")[0]
        aisrt_file = f"{path.splitext(aitxt_file)[0]}.aisrt"
        ref_srt_file = path.join(aitxt_dir, f"{basename}-{ref_srt_lang}.srt")
        assert path.exists(ref_srt_file)
        aitxt_to_aisrt(
            aitxt_file=aitxt_file,
            aisrt_file=aisrt_file,
            ref_srt_lang=ref_srt_lang,
        )

if __name__ == "__main__":
    #-------------------
    aitxt_dir = "D:/output"
    suffix=".aitxt"
    ref_srt_lang="en"
    aitxts_to_aisrts(
        aitxt_dir=aitxt_dir,
        suffix=suffix,
        ref_srt_lang=ref_srt_lang
    )