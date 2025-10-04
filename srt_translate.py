import os
import glob

from edge_srt_to_speech.__main__ import _main
import pysrt
import asyncio

srt_dir = "subtitles"
out_dir = "output"
if os.path.exists(out_dir):
    os.makedirs(out_dir)

for srt_file in glob.glob(os.path.join(srt_dir, "**/*zh.srt"), recursive=True):
    basename = os.path.basename(srt_file).split("-")[0]
    out_file = f"{out_dir}/{basename}-zh.mp3"

    print(f"generate mp3: {out_file}")
    asyncio.get_event_loop().run_until_complete(_main(
        srt_data = pysrt.open(srt_file),
        voice = "zh-CN-XiaoxiaoNeural",
        out_file = out_file,
        rate = "+0%",
        volume = "+0%",
        batch_size = 50,
        enhanced_srt = False,
    ))
