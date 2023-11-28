# 必要なモジュールをインポート
from requests import Response
import csv
import schedule
import time

# 自作のモジュールをインポート
from lib.wordpress.post import post as wp_post, create_wordpress_post_html
from lib.icatch.create_and_push import create_and_upload

def execute():
    gpt_model = "gpt-3.5-turbo"  # 追加
    main_keyword = "golang"

    # find keyword to seo-keyword-files in csv file.
    # and get the first line. and get the keyname "キーワード" to keyword_string variable. and delete the first line.
    # CSVファイルからキーワードを取得
    keyword_string = ""
    reader = None
    csv_file_path = f'seo-keyword-files/{main_keyword}.csv'

    with open(csv_file_path, newline='', encoding='utf-8', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('isPosted') == "1":
                continue
            keyword_string = row.get('キーワード', '')
            break  # 最初の行のみ取得
        

    temp_csv_file_path = f'{csv_file_path}.temp'
    # 変更後のデータを一時ファイルに書き込みます。
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile, open(temp_csv_file_path, 'w', newline='', encoding='utf-8') as tempfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
        
        # CSVファイルのヘッダーを書き込みます。
        writer.writeheader()

        # 各行を処理します。
        for row in reader:
            # 指定のキーワードが見つかった場合、isPostedを1に設定します。
            if row['キーワード'] == keyword_string:
                row['isPosted'] = '1'
            writer.writerow(row)

    # 一時ファイルを元のファイルに置き換えます。
    import os
    os.replace(temp_csv_file_path, csv_file_path)

    # create request message
    prompt_message = f"""
    「{keyword_string}」のキーワードで小学生でもわかる様に丁寧に解説するための記事を書いてください。
    ■制約
    ・マークダウン形式で作成してください
    ・キーワードに関する作成した記事のみを回答として出力してください。
    """
    post_title = f"{keyword_string}について小学生でもわかる様に解説！"
    icatch_title = keyword_string
    print("-------- prompt message ------------")
    print(prompt_message)
    print("-------- post title ------------")
    print(post_title)
    print("-------- icatch title ------------")
    print(icatch_title)

    # データをファイルに書き込む
    with open(os.getenv("INPUT_API_REQUEST_PATH"), "w") as fp:
        fp.write(prompt_message)
    with open(os.getenv("INPUT_POST_TITLE_PATH"), "w") as fp:
        fp.write(post_title)
    with open(os.getenv("INPUT_ICATCH_TITLE_PATH"), "w") as fp:
        fp.write(icatch_title)

    print("-------- creating and postring post message .... ------------")
    # WordPressに投稿
    res: Response = wp_post(
        create_wordpress_post_html,
        os.getenv("WORDPRESS_BASE_URL") + os.getenv("WORDPRESS_CONTENT_POST_ENTRY_POINT"),
        os.getenv("WORDPRESS_API_USERNAME"),
        os.getenv("WORDPRESS_API_PASSWORD"),
        gpt_model,  # 追加
        media_id=create_and_upload(os.getenv("INPUT_ICATCH_TITLE_PATH"))
    )

    if res.status_code == 201:
            res_json = res.json()
            posted_url = res_json['link']
            print(posted_url)
    else:
        error_msg = res.content.decode("utf-8")
        print(error_msg)

if __name__ == "__main__":
    # 日本時間で夜の７時、８じ、９時にexecute関数を実行する様にセットする
    schedule.every().day.at(f"19:00").do(execute)
    schedule.every().day.at(f"19:30").do(execute)
    schedule.every().day.at(f"20:00").do(execute)
    while True:
        schedule.run_pending()
        time.sleep(1)