import requests
import shutil


def img_download(img_url, save_filepath):
    res = requests.get(img_url, stream=True)
    if res.status_code == 200:
        with open(save_filepath, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        return True
    else:
        return False
