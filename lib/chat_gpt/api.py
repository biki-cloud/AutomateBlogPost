from logging import getLogger
import os

import openai

from lib.utils.markdown import to_html

logger = getLogger(__name__)


def chat_GPT_API(request_message: str) -> str:
    openai.api_key = os.getenv("CHAT_GPT_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": request_message},  # ※1後述
        ]
    )
    return response["choices"][0]["message"]["content"]  # 返信のみを出力


def use_chat_GPT_API(request_message, api_response_path):
    logger.info("chat gpt api start ...")
    logger.info(f"request_message: {request_message}")
    print(request_message)
    res = chat_GPT_API(request_message)
    with open(api_response_path, "w") as fp:
        fp.write(res)
    print("chat gpt api end ...")
    html = to_html(res)
    return html


if __name__ == "__main__":
    # with open("./gpt-text.txt", 'r') as fp:
    #     content = fp.read()
    response = chat_GPT_API("pythonのdictについての説明をhtmlフォーマットで出力して")
    print(response)
