import os
from os import path
import glob
import argparse
import re
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
    
    # 读取 aitxt 所有行，并解析带行号的行
    regex = re.compile(r"^(?P<seq>\d+)[\.\s]+(?P<text>.*)$")
    with open(aitxt_file, 'r', encoding="utf-8") as file:
        ai_lines = file.readlines()
        ai_lines = [line.strip() for line in ai_lines if len(line.strip()) > 0]
        ai_lines = [line for line in ai_lines if regex.match(line)]
    
    # 读取参考字幕的条目
    aitxt_dir = path.dirname(aitxt_file)
    basename = path.basename(aitxt_file).split("-")[0]
    ref_srt_file = path.join(aitxt_dir, f"{basename}-{ref_srt_lang}.srt")
    assert path.exists(ref_srt_file)
    ref_subs = pysrt.open(ref_srt_file)
    
    # 断言 aitxt 行和参考字幕的行数相等
    print(f"{path.basename(aitxt_file)}: {len(ai_lines)}, {path.basename(ref_srt_file)}: {len(ref_subs)}")
    assert len(ai_lines) == len(ref_subs)
    
    # 创建aisrt字幕文件
    for ref_sub in ref_subs:
        ai_line = ai_lines[ref_sub.index - 1]
        res = regex.match(ai_line)
        ai_seq = int(res.group("seq"))
        assert ai_seq == ref_sub.index
        ref_sub.text = res.group("text")
        print(f"{ai_seq:03d} [{ref_sub.start} --> {ref_sub.end}] {ref_sub.text}")
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
    parser = argparse.ArgumentParser(description="deepseek txt to aisrt")
    parser.add_argument("--aitxt_dir", help="aitxt dir", default="subtitles")
    parser.add_argument("--suffix", help="filename suffix", default=".aitxt")
    parser.add_argument("--ref_srt_lang", help="ref srt lang", default="en")
    args = parser.parse_args()

    aitxts_to_aisrts(
        aitxt_dir    = args.aitxt_dir,
        suffix       = args.suffix,
        ref_srt_lang = args.ref_srt_lang,
    )