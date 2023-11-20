import os

from lib.icatch.create_icatch import create
from lib.wordpress.media_upload import wp_upload_media

OUTPUT_DIR = "assets/img_tmp"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "tmp.jpg")


def create_and_upload(title_path):
    create(title_path, OUTPUT_PATH)
    return wp_upload_media(OUTPUT_PATH)


if __name__ == "__main__":
    create_and_upload("../assets/user_input/icatch_title.txt")
