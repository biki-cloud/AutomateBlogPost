import requests

# モジュールをインポート
import requests
import json

# アクセス情報の設定
AUTH_USER = 'hibiki'
AUTH_PASS = 'uHn2 OD9s rWFI ItC1 Fs77 IdME'

# 投稿するURLの設定
END_POINT_URL = "https://www.tukatech.jp/techblog/wp-json/wp/v2/posts"

# 投稿内容
p_title = "PythonからのWP REST API経由での投稿です"
p_content = 'PythonからのWP REST API経由での投稿です。' # javascriptは埋め込むことができなそう
p_status = "publish"

with open('assets/posted/wordpress_post.html') as fp:
    p_content += fp.read()

payload = {
            'title': p_title ,
            'content' : p_content ,
            'status' : p_status,
            'slug' : 'python_wp_rest_api_post'
            }

headers = {'content-type': "Application/json"}

r = requests.post( END_POINT_URL, data=json.dumps(payload) , headers=headers, auth=(AUTH_USER, AUTH_PASS) )
print(r)
print(r.content.decode("utf-8"))