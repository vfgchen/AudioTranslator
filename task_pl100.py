from os import path
from deepseek_txt_to_aitxt import txt_ai_translate_async
from deepseek_txt_to_aitxt import build_async_client
import argparse
import asyncio
import os

# 分组生成器
def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

async def main():
    root_dir = "subtitles"
    def resolve(item): return path.join(root_dir, item)

    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--api_key", help="app_key", default="")
    args = parser.parse_args()

    # 读取任务
    with open(resolve("task.txt"), "r", encoding="utf-8") as file:
        filenames = [item.strip() for item in file.readlines() if len(item.strip()) > 0]
    
    # 构建 chat_client
    api_key = args.api_key
    if api_key == "":
        api_key = os.environ.get('DEEPSEEK_API_KEY')
    chat_client = build_async_client(api_key=api_key)

    # 异步分批执行
    for batch in batch_generator(filenames, 5):
        print(f"exec batch: {",".join(batch)}")
        tasks = [
            asyncio.create_task(txt_ai_translate_async(
                txt_file=resolve(filename),
                chat_client=chat_client,
                topic="Power Platform: PL-100",
            )) for filename in batch
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
