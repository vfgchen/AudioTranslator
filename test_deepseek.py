from os import path
from deepseek_txt_to_aitxt import build_client, txt_ai_translate

txt_file=path.join("./subtitles", "001-en.txt")

content_file, reasoning_file = txt_ai_translate(
    txt_file    = txt_file,
    chat_client = build_client(),
    topic       = "Power Platform: PL-100"
)

