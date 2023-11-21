import json
import requests
import os
from lib.chat_gpt.api import use_chat_GPT_API

# wordpress post API
# https://developer.wordpress.com/docs/api/1.1/post/sites/%24site/media/new/


def post(create_content_func, post_api_url, API_USERNAME, API_PASSWORD, media_id=None):
    request_filepath = os.getenv("INPUT_API_REQUEST_PATH")
    print(f"request file: {request_filepath}")
    print(post_api_url)
    print(API_USERNAME + " " + API_PASSWORD)

    with open(os.getenv("INPUT_POST_TITLE_PATH"), "r") as fp:
        title = fp.read()
    # 送信する記事データ
    # TODO: contentの内容次第で403エラーになる。長いのか？試しにtest.pyで試してみる。
    post_data = {
        'title': title,
        'content': create_content_func(request_filepath),
        # 'content': 'xxxxxx',
        'slug': title,
        'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる,
        # 'categories': 4, # カテゴリーIDが入る
        # 'featured_media': media_id # アップロードした画像のIDが入る
    }

    def do_post():
        print("wordpress posting start ...")

        headers = {'content-type': "Application/json"}
        res = requests.post(post_api_url, 
                            data=json.dumps(post_data),
                            headers=headers,
                            auth=(API_USERNAME, API_PASSWORD)
                            )
        print(f"Result: {res.status_code}")

        if res.status_code == 201:
            print("Successful")
            print(res.json())
        else:
            print("failed")
            print(res.content.decode("utf-8"))
        print("wordpress posting end ...")
        return res

    return do_post()


def create_wordpress_post_html(request_filepath) -> str:
    api_question = open(request_filepath).read()

    content = ""
    post_html = use_chat_GPT_API(api_question, os.getenv("OUTPUT_CHAT_GPT_RESPONSE_PATH"))
    content += post_html
    with open("assets/affiliates/affiliate.html") as fp:
        content += fp.read()
    with open(os.getenv("OUTPUT_POSTED_HTML_PATH"), "w") as fp:
        fp.write(content)
    return content
