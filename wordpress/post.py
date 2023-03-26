import requests
import os
from chat_gpt.api import use_chat_GPT_API

# wordpress post API
# https://developer.wordpress.com/docs/api/1.1/post/sites/%24site/media/new/


def post(create_content_func, post_api_url, API_USERNAME, API_PASSWORD, media_id):
    request_filepath = os.environ["request_path"]
    print(f"request file: {request_filepath}")

    with open(os.environ["wp_post_title_path"], "r") as fp:
        title = fp.read()
    # 送信する記事データ
    post_data = {
        'title': title,
        'content': create_content_func(request_filepath),
        'slug': title,
        'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる,
        'categories': 4,
        'featured_media': media_id
    }

    def do_post():
        print("wordpress posting start ...")
        # 記事投稿リクエスト
        res = requests.post(
            post_api_url,
            json=post_data,
            auth=(API_USERNAME, API_PASSWORD),
            timeout=1
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
    post_html = use_chat_GPT_API(api_question, os.environ["cg_api_response_path"])
    content += post_html
    with open("assets/affiliates/affiliate.html") as fp:
        content += fp.read()
    with open("assets/posted/wordpress_post.html", "w") as fp:
        fp.write(content)
    return content
