from flask import Flask, render_template, request
from env import setenv
import os
from requests import Response

from wordpress.post import post as wp_post, create_wordpress_post_html
from icatch.create_and_push import create_and_upload

app = Flask(__name__)


@app.route('/')
def home():
    api_request = ""
    post_title = ""
    icatch_title = ""
    with open(os.environ["input_api_request"], "r") as fp:
        api_request = fp.read()
    with open(os.environ["input_post_title"], "r") as fp:
        post_title = fp.read()
    with open(os.environ["input_icatch_title"], "r") as fp:
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
    print(api_request)
    print(post_title)
    print(icatch_title)
    # 書き込み
    with open(os.environ["input_api_request"], "w") as fp:
        fp.write(api_request)
    with open(os.environ["input_post_title"], "w") as fp:
        fp.write(post_title)
    with open(os.environ["input_icatch_title"], "w") as fp:
        fp.write(icatch_title)
    res: Response = wp_post(
        create_wordpress_post_html,
        os.environ["wp_post_url"],
        os.environ["wp_api_username"],
        os.environ["wp_api_password"],
        create_and_upload(os.environ["input_icatch_title"])
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
    setenv()
    app.run(debug=True)