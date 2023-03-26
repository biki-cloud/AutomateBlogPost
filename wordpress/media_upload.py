import requests
import os
import json


def wp_upload_media(file_path):
    url_base = os.environ["wp_base_url"]
    url = f"{url_base}/wp-json/wp/v2/media/"

    user = os.environ['wp_api_username']  # ユーザー名
    password = os.environ['wp_api_password']  # アプリケーションパスワードで発行したパスワード

    f = open(file_path, 'rb')
    image_data = f.read()
    f.close()

    filename = os.path.basename(file_path)
    print(filename)
    headers = {
        'Content-Type': 'image/png',
        'Content-Disposition': 'attachment; filename=' + filename,
    }

    res = requests.post(
        url,
        data=image_data,
        headers=headers,
        auth=(user, password),
    )
    print(res)
    print(res.content.decode("utf-8"))
    res_dict = res.json()
    print(json.dumps(res_dict, indent=4))
    unique_id = res_dict['id']  # アップロードした画像のID
    return unique_id


if __name__ == "__main__":
    print(wp_upload_media("./test.png"))
