import os
import requests

# モジュールをインポート
import requests
import json

# アクセス情報の設定
AUTH_USER = os.getenv("WORDPRESS_API_USERNAME")
AUTH_PASS = os.getenv("WORDPRESS_API_PASSWORD")

# 投稿するURLの設定
END_POINT_URL = os.getenv("WORDPRESS_BASE_URL") + os.getenv("WORDPRESS_CONTENT_POST_ENTRY_POINT")

# 投稿内容
p_title = "PythonからのWP REST API経由での投稿です"
p_content = 'PythonからのWP REST API経由での投稿です。' # javascriptは埋め込むことができなそう
p_status = "publish"

payload = {
            'title': p_title ,
            'content' : 'xxx',
            'status' : p_status,
            'slug' : 'python_wp_rest_api_post'
            }

headers = {'content-type': "Application/json"}

r = requests.post( END_POINT_URL, data=json.dumps(payload) , headers=headers, auth=(AUTH_USER, AUTH_PASS) )
print(r)
print(r.content.decode("utf-8"))