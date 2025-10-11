# Please install OpenAI SDK first: `pip3 install openai`
import os
import glob
import argparse

from os import path
from typing import Dict
from openai import OpenAI

# 构建 deepseek 提示词
def build_prompt(
        input_text : str,
        context_info: Dict = None
    ):
    """
    content_info
        topic : 主题领域
        proper_nouns : [...专有名称]
        style : 语言风格
    """
    context_str = ""
    if 'topic' in context_info:
        context_str += f"主题领域：{context_info['topic']}\n"
    if 'proper_nouns' in context_info:
        context_str += f"专有名词：{', '.join(context_info['proper_nouns'])}\n"
    if 'style' in context_info:
        context_str += f"语言风格：{context_info['style']}\n"
    return f"""
你是一名专业的字幕校对专家。请对以下语音识别生成的文本进行纠错和润色。

{context_str}

## 纠错要求：
1. **纠正同音字和错别字**：重点修正语音识别常见的同音字错误
2. **修正语法和标点**：使句子通顺，符合英文和中文语法规范
3. **保持口语化流畅**：保留口语的自然感，但删除无意义的重复词和语气词，
4. **统一专有名词**：确保术语、人名、地名前后一致
5. **基于上下文补全逻辑**：对识别不全的句子进行合理补全
6. **绝对保持原意**：不能改变说话者的原本意图
7. **保留段落行号**：给输入每一行编号，即使纠错后内容为空，行号依然保留

## 输入文本：
{input_text}

## 输出要求：
1. 输出修正后的英文完整文本
2. 输出中文完整文本
3. 文本段落开头输出行号
4. 不需要额外解释
5. 严格保持输出和输入的段落结构一致，请严格保持输入输出行数一致
"""

# deepseek client
def build_client(
        api_key : str = os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com"
    ):
    return OpenAI(api_key=api_key, base_url=base_url)

# txt to req
def txt_to_req(
        txt_file,
        req_file,
        context_info: Dict = None,
    ):
    # 创建 req_file 所在目录
    if not path.exists(path.dirname(req_file)):
        os.makedirs(path.dirname(req_file))
    # 读取 txt_file
    with open(txt_file, "r", encoding="utf-8") as file:
        input_text = file.read()
    # 构建提示文本
    input_content = build_prompt(
        input_text=input_text,
        context_info=context_info
        )
    # 保持到 req_file
    with open(req_file, "w", encoding="utf-8") as file:
        file.write(input_content)
    print(f"txt_to_req, save: {req_file}")
    return req_file

# deepseek ai translate
def text_ai_translate(
        input_text: str,
        context_info: Dict = None,
        chat_client: OpenAI = None,
        model: str = "deepseek-reasoner"
        ):
    """
    req_file: 暂存发送deepseek请求的文件
    model:
        deepseek-chat
        deepseek-reasoner
    """
    # 提示文本
    input_content = build_prompt(
        input_text=input_text,
        context_info=context_info
        )
    # 输出内容
    print(f"\ntext_ai_translate, send:\n{input_content}")
    response = chat_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{input_content}"},
        ],
        stream=False
    )
    # 输出文本
    content = response.choices[0].message.content
    print(f"\ntext_ai_translate, receive:\n{content}")
    # 思考文本
    try:
        reasoning_content = response.choices[0].message.reasoning_content
    except:
        print("warn text_ai_translate: no reasoning_content")
        reasoning_content = ""
    return content, reasoning_content

# deepseek txt file ai translate
def txt_ai_translate(
        txt_file,
        chat_client,
        topic,
        model="deepseek-reasoner",
    ):
    # 构建翻译上下文信息
    context_info = dict()
    if topic: context_info["topic"] = topic

    # txt to req, 生成***-en.req
    req_file = f"{path.splitext(txt_file)[0]}.req"
    txt_to_req(
        txt_file=txt_file,
        req_file=req_file,
        context_info=context_info)
    
    # 读取txt文件内容并发送给ai翻译
    with open(txt_file, "r", encoding="utf-8") as txt:
        input_text = txt.read()
    content, reasoning = text_ai_translate(
        input_text=input_text,
        context_info=context_info,
        chat_client=chat_client,
        model=model,
    )

    # 保存deepseek输出内容，思考内容
    content_file = f"{path.splitext(txt_file)[0]}.content"
    reasoning_file = f"{path.splitext(txt_file)[0]}.reasoning"
    if content != "":
        with open(content_file, "w", encoding="utf-8") as file:
            file.write(content)
            print(f"txt_ai_translate, content file: {content_file}")
    if reasoning != "":
        with open(reasoning_file, "w", encoding="utf-8") as file:
            file.write(reasoning)
            print(f"txt_ai_translate, reasoning file: {reasoning_file}")
    return content_file, reasoning_file

# 解析 AI Chat 输出内容
def content_to_aitxt(
        content_file
    ):
    # 读取文件内容
    assert path.exists(content_file)
    with open(content_file, "r", encoding="utf-8") as file:
        content = file.read()
    # 解析输出内容中英文和中文内容
    en_lines = []
    zh_lines = []
    all_lines = [line.strip() for line in content.split("\n") if len(line.strip()) > 0]
    for index, line in enumerate(all_lines):
        if index < len(all_lines) / 2:
            en_lines.append(line)
        else:
            zh_lines.append(line)
    # 保存英文和中文文本
    txt_dir = path.dirname(content_file)
    basename = path.basename(content_file).split("-")[0]
    en_aitxt_file = path.join(txt_dir, f"{basename}-en.aitxt")
    zh_aitxt_file = path.join(txt_dir, f"{basename}-zh.aitxt")
    with open(en_aitxt_file, "w", encoding="utf-8") as file:
        for line in en_lines:
            file.write(f"{line}\n")
        print(f"content_to_aitxt en: {en_aitxt_file}")
    with open(zh_aitxt_file, "w", encoding="utf-8") as file:
        for line in zh_lines:
            file.write(f"{line}\n")
        print(f"content_to_aitxt zh: {zh_aitxt_file}")
    return en_aitxt_file, zh_aitxt_file

# txt to aitxt
def txt_to_aitxt(
        txt_file,
        chat_client,
        topic,
        model="deepseek-reasoner",
    ):
    # AI 翻译
    content_file, reasoning_file = txt_ai_translate(
        txt_file=txt_file,
        chat_client=chat_client,
        topic=topic,
        model=model
    )
    # 生成 aitxt 文件
    en_aitxt_file, zh_aitxt_file = content_to_aitxt(
        content_file=content_file
    )
    print(f"txt_to_aitxt en: {txt_file} -> {en_aitxt_file}")
    print(f"txt_to_aitxt zh: {txt_file} -> {zh_aitxt_file}")
    return en_aitxt_file, zh_aitxt_file

def txts_to_reqs(
        txt_dir="subtitles",
        suffix="en.txt",
        context_info: Dict = None,
    ):
    for txt_file in glob.glob(path.join(txt_dir, f"**/*{suffix}"), recursive=True):
        req_file = f"{path.splitext(txt_file)[0]}.req"
        txt_to_req(
            txt_file=txt_file,
            req_file=req_file,
            context_info=context_info,
        )

# txts to aitxts
def txts_to_aitxts(
        txt_dir="subtitles",
        suffix="en.txt",
        chat_client=None,
        topic=None,
        model="deepseek-reasoner",
        delete_txt_file=True,
    ):
    for txt_file in glob.glob(path.join(txt_dir, f"**/*{suffix}"), recursive=True):
        txt_to_aitxt(
            txt_file=txt_file,
            chat_client=chat_client,
            topic=topic,
            model=model,
        )
        if delete_txt_file:
            os.remove(txt_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="deepseek txt to aisrt")
    parser.add_argument("--txt_dir", help="txt dir", default="subtitles")
    parser.add_argument("--suffix", help="filename suffix", default="en.txt")
    parser.add_argument("--topic", help="ai translate topic", default="Power Platform")
    parser.add_argument("--model", help="deepseek model", choices=["deepseek-chat", "deepseek-reasoner"], default="deepseek-reasoner")
    parser.add_argument("--delete_txt_file", help="delete txt file on success", default="no")
    parser.add_argument("--api_key", help="deepseek api key", default="")
    parser.add_argument("--base_url", help="deepseek api key", default="https://api.deepseek.com")
    args = parser.parse_args()

    api_key = args.api_key
    if api_key == "":
        api_key = os.environ.get('DEEPSEEK_API_KEY')
    assert api_key != ""

    chat_client = build_client(
        api_key     = api_key,
        base_url    = "https://api.deepseek.com",
    )

    delete_txt_file = args.delete_txt_file.lower() in ["yes", "y", "true"]
    txts_to_aitxts(
        txt_dir     = args.txt_dir,
        suffix      = args.suffix,
        chat_client = chat_client,
        topic       = args.topic,
        model       = args.model,
        delete_txt_file = delete_txt_file
    )
