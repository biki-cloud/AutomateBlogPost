import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

IMG_Q = 90
IMG_SIZE = (780, 428)
TEXT_SIXE = (750, 200)
TEXT_MARGIN = 30
MAX_FONT_SIZE = 100
FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
TEXT_COLORS = (
    ('1', '#19A7CE', (246, 241, 241)),
    ('2', '#2B3467', (186, 215, 233))
)


def make_eye_catch(img_path, output_path, text):
    # 画像のファイル名を取得
    file_name, ext = os.path.splitext(img_path)
    # \n（改行指定）でテキストを分割
    text = text.split(r"\n")

    # 先に文字の描画領域決定。合わせて下記を計算しておく
    # フォントサイズfont_size, 描画幅area_width, 描画高さarea_height, lines_size
    for font_size in range(MAX_FONT_SIZE, 9, -1):

        # フォント
        font = ImageFont.truetype(FONT_PATH, font_size)

        # 各行の[幅、高さ]を計算
        lines_size = [list(font.getsize(t)) for t in text]

        # 幅の最大と高さの合計
        area_x = np.max(lines_size, 0)[0]
        area_y = np.sum(lines_size, 0)[1]

        if (area_x <= TEXT_SIXE[0] and area_y <= TEXT_SIXE[1]):
            break

    # 画像読み込み、サイズ取得
    img = Image.open(img_path)
    original_img_size = img.size

    # 縮小
    if (original_img_size[0] / original_img_size[1]) \
            >= (IMG_SIZE[0] / IMG_SIZE[1]):
        # 目標より横長なら、縦横比を維持して、縦を目標まで縮める
        img.thumbnail((original_img_size[0], IMG_SIZE[1]))
        thumbnail_size = img.size
        # 横幅を切り取るための計算をする
        crop_left = int((thumbnail_size[0] - IMG_SIZE[0]) / 2)
        crop_upper = 0
        crop_right = crop_left + IMG_SIZE[0]
        crop_lower = IMG_SIZE[1]
    else:
        # 目標より縦長なら、縦横比を維持して、横を目標まで縮める
        img.thumbnail((IMG_SIZE[0], original_img_size[1]))
        thumbnail_size = img.size
        # 縦幅を切り取るための計算をする
        crop_left = 0
        crop_upper = int((thumbnail_size[1] - IMG_SIZE[1]) / 2)
        crop_right = IMG_SIZE[0]
        crop_lower = crop_upper + IMG_SIZE[1]

    # 計算した縦横で切り取る
    img = img.crop((crop_left, crop_upper, crop_right, crop_lower))

    # 背景の塗りつぶしと文字書き込み準備
    rectangle_y = area_y + TEXT_MARGIN
    rectangle_top = int((IMG_SIZE[1] - rectangle_y) / 2)

    # 白黒２色分画像を作成
    for (label, fg_color, bg_color) in TEXT_COLORS:
        # 塗りつぶし領域作成
        rectangle_img = Image.new('RGBA', img.size)
        draw = ImageDraw.Draw(rectangle_img)
        draw.rectangle((0, rectangle_top, IMG_SIZE[0],
                        rectangle_top + rectangle_y), bg_color)

        # 塗りつぶし
        org_img = img.convert('RGBA')
        new_img = Image.alpha_composite(org_img, rectangle_img)

        draw = ImageDraw.Draw(new_img)
        _y = int((IMG_SIZE[1] - area_y) / 2)
        for (t, line) in zip(text, lines_size):
            _x = int((IMG_SIZE[0] - line[0]) / 2)
            draw.text((_x, _y), t, font=font, fill=fg_color)
            _y += line[1]

        new_img = new_img.convert("RGB")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        new_img.save(output_path, quality=IMG_Q)
        plt.figure()
        plt.imshow(new_img)

        return True


if __name__ == "__main__":
    txt = """python requestsライブラリ 使用方法"""
    output_path = make_eye_catch(
        "input/python.jpg",
        "pro1/output/test.jpg",
        txt)
    print(output_path)
