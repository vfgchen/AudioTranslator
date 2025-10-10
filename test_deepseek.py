# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

input_content = """
你是一名专业的字幕校对专家。请对以下语音识别生成的文本进行纠错和润色。

主题领域: Microsoft PL-100

## 纠错要求：
1. **纠正同音字和错别字**：重点修正语音识别常见的同音字错误
2. **修正语法和标点**：使句子通顺，符合中文语法规范
3. **保持口语化流畅**：保留口语的自然感，但删除无意义的重复词和语气词
4. **统一专有名词**：确保术语、人名、地名前后一致
5. **基于上下文补全逻辑**：对识别不全的句子进行合理补全
6. **绝对保持原意**：不能改变说话者的原本意图

## 输入文本：
Yeah.
Hi, everyone.
Welcome to this power platform course.
With over 20 years of experience and data across a range of industries.
I know it takes to be effective.
I'm Philip Burton of I do Datata dot com, and I'll be your instructor for this course.
Data is all around us.
The ability to present and manipulate data is the key to unlocking business potential.
These skills are now at your fingertips.
This 16 hour Microsoft Power platform apps make a calls.
Covers the requirements for the P, L 100 exam.


## 输出要求：
请先直接返回修正后的英文完整文本，再输出中文完整文本，英文和中文文本之间用一行空行分隔，不需要额外解释。保持原文的段落结构。
"""

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": f"{input_content}"},
        # {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response)
print(response.choices[0].message.content)

output_content    = response.choices[0].message.content
reasoning_content = response.choices[0].message.reasoning_content

with open("./deepseek-output_content.txt", "w", encoding="utf-8") as file:
    file.write(output_content)

with open("./deepseek-reasoning_content.txt", "w", encoding="utf-8") as file:
    file.write(reasoning_content)
