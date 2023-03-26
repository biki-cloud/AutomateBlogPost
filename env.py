import os


def setenv():
    project_dir = os.getcwd()
    assets_dir = os.path.join(project_dir, "assets")
    print(assets_dir)
    os.environ["request_path"] = os.path.join(assets_dir, "user_input/api_request.txt")
    os.environ["wp_base_url"] = "https://tuka.conohawing.com/tuka-blog"
    os.environ["wp_api_username"] = "hibiki"
    os.environ["wp_api_password"] = "ZUYV Z1lW 2Rw1 3rrG Hyia PacK"
    os.environ["wp_post_url"] = os.environ["wp_base_url"] + "/wp-json/wp/v2/posts"
    os.environ["wp_media_post_url"] = os.environ["wp_base_url"] + "/wp-json/wp/v2/media/"
    os.environ["wp_post_title_path"] = assets_dir + "/user_input/post_title.txt"
    os.environ["cg_key"] = "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"
    os.environ["cg_api_response_path"] = assets_dir + "/posted/api-response.txt"
    os.environ["input_api_request"] = assets_dir + "/user_input/api_request.txt"
    os.environ["input_post_title"] = assets_dir + "/user_input/post_title.txt"
    os.environ["input_icatch_title"] = assets_dir + "/user_input/icatch_title.txt"
