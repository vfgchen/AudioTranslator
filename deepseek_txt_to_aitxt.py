# Please install OpenAI SDK first: `pip3 install openai`
import os
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
2. **修正语法和标点**：使句子通顺，符合中文语法规范
3. **保持口语化流畅**：保留口语的自然感，但删除无意义的重复词和语气词
4. **统一专有名词**：确保术语、人名、地名前后一致
5. **基于上下文补全逻辑**：对识别不全的句子进行合理补全
6. **绝对保持原意**：不能改变说话者的原本意图

## 输入文本：
{input_text}

## 输出要求：
请先直接返回修正后的英文完整文本，再输出中文完整文本，英文和中文文本之间用一行空行分隔，不需要额外解释。保持原文的段落结构。
"""

# deepseek client
def build_client(
        api_key : str = os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com"
    ):
    return OpenAI(api_key=api_key, base_url=base_url)

# deepseek ai translate
def text_ai_translate(
        input_text: str,
        context_info: Dict = None,
        chat_client: OpenAI = None,
        model: str = "deepseek-reasoner"
        ):
    """
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
    response = chat_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"{input_content}"},
        ],
        stream=False
    )
    # 输出文本
    content = response.choices[0].message.content
    # 思考文本
    try:
        reasoning_content = response.choices[0].message.reasoning_content
    except:
        print("warn: no reasoning_content")
        reasoning_content = ""
    return content, reasoning_content

# deepseek txt file ai translate
def txt_ai_translate(
        txt_file,
        chat_client,
        topic,
        model="deepseek-chat",
    ):
    # 读取输入文件文本
    with open(txt_file, "r", encoding="utf-8") as txt:
        input_text = txt.read()
    # 文本翻译
    context_info = dict()
    if topic: context_info["topic"] = topic
    content, reasoning = text_ai_translate(
        input_text=input_text,
        context_info=context_info,
        chat_client=chat_client,
        model=model
    )
    # 保存deepseek输出内容，思考内容
    txt_dir = path.dirname(txt_file)
    # basename = path.basename(txt_file).split("-")[0]
    basename = path.splitext(txt_file)[0]
    content_file = path.join(txt_dir, f"{basename}.content")
    reasoning_file = path.join(txt_dir, f"{basename}.reasoning")
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
        model="deepseek-chat",
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

if __name__ == "__main__":
    #-------------------
    chat_client = build_client()

    #-------------------
    # content_file, reasoning_file = txt_ai_translate(
    #     txt_file="D:/output/001-en.txt",
    #     chat_client=chat_client,
    #     topic="Microsoft: PL-100",
    #     model="deepseek-chat",
    #     )

    #-------------------
    # en_aitxt_file, zh_aitxt_file = content_to_aitxt(
    #     content_file="D:/output/001-en.content"
    # )

    #-------------------
    en_aitxt_file, zh_aitxt_file = txt_to_aitxt(
        txt_file="D:/output/001-en.txt",
        chat_client=chat_client,
        topic="Microsoft: PL-100",
        model="deepseek-chat",
    )
