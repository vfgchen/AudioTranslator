from os import path
from deepseek_txt_to_aitxt import txt_ai_translate
from deepseek_txt_to_aitxt import build_client
import argparse

root_dir = "subtitles"
def resolve(item): return path.join(root_dir, item)

parser = argparse.ArgumentParser(description="audio to srt")
parser.add_argument("--api_key", help="app_key", default="")
args = parser.parse_args()

# 读取任务
with open(resolve("task.txt"), "r", encoding="utf-8") as file:
    tasks = file.readlines()
chat_client = build_client(api_key=args.api_key)
for task in tasks:
    txt_file = resolve(task)
    content_file, reasoning_file = txt_ai_translate(
        txt_file=txt_file,
        chat_client=chat_client,
        topic="Power Platform: PL-100",
    )
