import openai
import shutil
import requests
from config import GPT_KEY

openai.api_key = GPT_KEY

response = openai.Image.create(
  prompt="pythonのrequestsライブラリの使用方法というブログのアイキャッチ画像",
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

file_name = "../../output.jpg"
print(image_url)
res = requests.get(image_url, stream = True)
if res.status_code == 200:
    with open(file_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ',file_name)
else:
    print('Image Couldn\'t be retrieved')