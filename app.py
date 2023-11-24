# 必要なモジュールをインポート
from flask import Flask, render_template, request
import os
from requests import Response
import logging
import urllib.parse

# 自作のモジュールをインポート
from lib.wordpress.post import post as wp_post, create_wordpress_post_html
from lib.icatch.create_and_push import create_and_upload

# Flaskアプリケーションを作成
app = Flask(__name__)

# ロガーを作成
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # ロガーをdebugに設定

# ホームページのルート
@app.route('/')
def home():
    # 前回の入力内容を読み込む
    api_request = ""
    post_title = ""
    icatch_title = ""
    with open(os.getenv("INPUT_API_REQUEST_PATH"), "r") as fp:
        api_request = fp.read()
    with open(os.getenv("INPUT_POST_TITLE_PATH"), "r") as fp:
        post_title = fp.read()
    with open(os.getenv("INPUT_ICATCH_TITLE_PATH"), "r") as fp:
        icatch_title = fp.read()

    # index.htmlをレンダリングして返す
    return render_template('index.html',
                           previous_api_request=api_request,
                           previous_post_title=post_title,
                           previous_icatch_title=icatch_title)

# ブログ投稿のルート
@app.route('/post', methods=['POST'])
def post():
    # フォームからデータを取得
    api_request = request.form['api_request']
    post_title = request.form['post_title']
    icatch_title = request.form['icatch_title']
    gpt_model = request.form['gpt-model']  # 追加
    logger.info({"api_request": api_request, "post_title": post_title, "icatch_title": icatch_title, "gpt_model": gpt_model})  # 更新

    # データをファイルに書き込む
    with open(os.getenv("INPUT_API_REQUEST_PATH"), "w") as fp:
        fp.write(api_request)
    with open(os.getenv("INPUT_POST_TITLE_PATH"), "w") as fp:
        fp.write(post_title)
    with open(os.getenv("INPUT_ICATCH_TITLE_PATH"), "w") as fp:
        fp.write(icatch_title)

    # WordPressに投稿
    res: Response = wp_post(
        create_wordpress_post_html,
        os.getenv("WORDPRESS_BASE_URL") + os.getenv("WORDPRESS_CONTENT_POST_ENTRY_POINT"),
        os.getenv("WORDPRESS_API_USERNAME"),
        os.getenv("WORDPRESS_API_PASSWORD"),
        # create_and_upload(os.getenv("INPUT_ICATCH_TITLE_PATH"))
    )
    posted_url = ""
    error_msg = ""
    res_json = ""
    if res.status_code == 201:
        res_json = res.json()
        posted_url = res_json['link']
    else:
        error_msg = res.content.decode("utf-8")
    return render_template('result.html',
                           status_code=res.status_code,
                           res_json=res_json,
                           posted_url=posted_url,
                           error_msg=error_msg
                           )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

