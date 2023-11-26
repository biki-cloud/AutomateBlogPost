from openai import OpenAI
import urllib.request
from PIL import Image

def generate_image(title, save_image_path):
    # add comment how to use this func
    """
    prompt: str
    save_image_path: str

    title = "python range"
    save_image_path = "./image.png"
    generate_image(prompt, save_image_path)
    """
    template_prompt = """
    create image representing "{}".
    Place the words "{}" in the center of the image.
    """
    # create prompt from template_prompt
    prompt = template_prompt.format(title, title)

    client = OpenAI()

    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1792x1024",
      quality="standard",
      n=1,
    )

    image_url = response.data[0].url

    # 画像を保存する
    urllib.request.urlretrieve(image_url, save_image_path)

    # 画像をアイキャッチ用にリサイズする
    image = Image.open(save_image_path)
    image = image.resize((1200, 630))
    image.save(save_image_path)

# call generate_image func in __main__
if __name__ == "__main__":
    prompt = """
    create image representing "python range".
    Place the words "python range" in the center of the image.
    """
    save_image_path = "./image.png"
    generate_image(prompt, save_image_path)