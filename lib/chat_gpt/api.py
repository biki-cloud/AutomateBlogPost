from logging import getLogger
import os

import openai
from openai import OpenAI

from lib.utils.markdown import to_html

logger = getLogger(__name__)

client = OpenAI(
    api_key=os.getenv("CHAT_GPT_API_KEY"),
)

def chat_GPT_API(request_message: str, gpt_model: str) -> str:  # gpt_modelを追加
    openai.api_key = os.getenv("CHAT_GPT_API_KEY")

    response = client.chat.completions.create(
        model=gpt_model,  # gpt_modelを使用
        messages=[
            {
                "role": "user",
                "content": request_message
            },  
            {
                "role": "system",
                "content": "あなたはSEOのプロフェッショナルです。日本語で返答してください。"
            },
        ]
    )
    return response.choices[0].message.content


def use_chat_GPT_API(request_message, api_response_path, gpt_model):  # gpt_modelを追加
    logger.info("chat gpt api start ...")
    logger.info(f"request_message: {request_message}")
    print(request_message)
    res = chat_GPT_API(request_message, gpt_model)  # gpt_modelを使用
    with open(api_response_path, "w") as fp:
        fp.write(res)
    print("chat gpt api end ...")
    html = to_html(res)
    return html


if __name__ == "__main__":
    # with open("./gpt-text.txt", 'r') as fp:
    #     content = fp.read()
    response = chat_GPT_API("pythonのdictについての説明をhtmlフォーマットで出力して", "gpt-3.5-turbo")  # gpt_modelを指定
    print(response)
