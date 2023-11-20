from lib.utils.img import img_download

TEMPLATE_PATH = "./assets/icatch/template_html.txt"


def create(title_path, output_path):
    with open(TEMPLATE_PATH, "r") as fp:
        base_url = fp.read()
    with open(title_path, "r") as fp:
        base_title = fp.read()
    title = base_title.replace(" ", "+")
    base_url = base_url.replace("***", title)
    img_download(base_url, output_path)


if __name__ == "__main__":
    create("../assets/user_input/icatch_title.txt", "test.png")
