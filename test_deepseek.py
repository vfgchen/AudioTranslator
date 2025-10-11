from os import path
from deepseek_txt_to_aitxt import build_client
from deepseek_txt_to_aitxt import txt_to_req
from deepseek_txt_to_aitxt import txts_to_reqs
from deepseek_txt_to_aitxt import txt_ai_translate
from deepseek_txt_to_aitxt import content_to_aitxt
from aitxt_to_aisrt import aitxt_to_aisrt
from srt_to_txt import srt_correct
from srt_to_txt import srt_to_txt

txt_dir="D:/output/subtitles"

# 生成 ***-en.req
suffix="en.txt"
context_info = dict()
context_info["topic"]="Power Platform: PL-100"
txts_to_reqs(
    txt_dir=txt_dir,
    suffix=suffix,
    context_info=context_info
)

# srt_correct
# srt_file = path.join(txt_dir, "017-en.srt")
# txt_file = path.join(txt_dir, "017-en.txt")
# srt_correct(srt_file)
# srt_to_txt(srt_file, txt_file, True)

# 生成 ***-en.content
# txt_file=path.join("./subtitles", "001-en.txt")
# content_file, reasoning_file = txt_ai_translate(
#     txt_file    = txt_file,
#     chat_client = build_client(),
#     topic       = "Power Platform: PL-100"
# )

# 生成 ***-en.aitxt
# 生成 ***-zh.aitxt
# content_file=path.join("./subtitles", "001-en.content")
# en_aitxt_file, zh_aitxt_file = content_to_aitxt(
#     content_file=content_file
# )

# 生成 ***-en.aisrt
# en_aitxt_file=path.join("./subtitles", "001-en.aitxt")
# en_aisrt_file=path.join("./subtitles", "001-en.aisrt")
# aitxt_to_aisrt(
#     aitxt_file=en_aitxt_file,
#     aisrt_file=en_aisrt_file,
#     ref_srt_lang="en"
# )

# 生成 ***-zh.aisrt
# zh_aitxt_file=path.join("./subtitles", "001-zh.aitxt")
# zh_aisrt_file=path.join("./subtitles", "001-zh.aisrt")
# aitxt_to_aisrt(
#     aitxt_file=zh_aitxt_file,
#     aisrt_file=zh_aisrt_file,
#     ref_srt_lang="en"
# )