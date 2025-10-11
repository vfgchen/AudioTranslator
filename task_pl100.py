from os import path
from deepseek_txt_to_aitxt import txt_ai_translate_async
from deepseek_txt_to_aitxt import build_async_client
import argparse
import asyncio

async def main():
    root_dir = "subtitles"
    def resolve(item): return path.join(root_dir, item)

    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--api_key", help="app_key", default="")
    args = parser.parse_args()

    # 读取任务
    with open(resolve("task.txt"), "r", encoding="utf-8") as file:
        tasks = [item for item in file.readlines() if len(item.strip()) > 0]
    chat_client = build_async_client(api_key=args.api_key)
    for task in tasks:
        txt_file = resolve(task.strip())
        print(f"task_pl100: {txt_file}")
        content_file, reasoning_file = await txt_ai_translate_async(
            txt_file=txt_file,
            chat_client=chat_client,
            topic="Power Platform: PL-100",
        )

if __name__ == "__main__":
    asyncio.run(main())
