# Chat GPT APIを実行する
from openai import OpenAI
import openai

# APIキーを設定する
openai.api_key = 'your-api-key'

# チャットモデルを使用してメッセージを生成する
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]
)

# レスポンスを出力する
print(response['choices'][0]['message']['content'])
