from flask import Flask, render_template, request
import os
from requests import Response
import logging
import urllib.parse

from lib.wordpress.post import post as wp_post, create_wordpress_post_html
from lib.icatch.create_and_push import create_and_upload

app = Flask(__name__)

logger = logging.getLogger(__name__)

@app.route('/')
def home():
    api_request = ""
    post_title = ""
    icatch_title = ""
    # 前回の入力内容を読み込み
    with open(os.getenv("INPUT_API_REQUEST_PATH"), "r") as fp:
        api_request = fp.read()
    with open(os.getenv("INPUT_POST_TITLE_PATH"), "r") as fp:
        post_title = fp.read()
    with open(os.getenv("INPUT_ICATCH_TITLE_PATH"), "r") as fp:
        icatch_title = fp.read()

    return render_template('index.html',
                           previous_api_request=api_request,
                           previous_post_title=post_title,
                           previous_icatch_title=icatch_title)


@app.route('/post', methods=['POST'])
def post():
    api_request = request.form['api_request']
    post_title = request.form['post_title']
    icatch_title = request.form['icatch_title']
    logger.info({"api_request": api_request, "post_title": post_title, "icatch_title": icatch_title})

    # 書き込み
    with open(os.getenv("INPUT_API_REQUEST_PATH"), "w") as fp:
        fp.write(api_request)
    with open(os.getenv("INPUT_POST_TITLE_PATH"), "w") as fp:
        fp.write(post_title)
    with open(os.getenv("INPUT_ICATCH_TITLE_PATH"), "w") as fp:
        fp.write(icatch_title)

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
