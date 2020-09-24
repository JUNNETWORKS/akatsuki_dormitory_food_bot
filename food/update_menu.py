"""
cron で1日1回実行するスクリプト

- 今月のデータがあるか
- 暁寮のHPのメニュー表が更新されているか
- 更新されてればメニュー表をDLし、それを画像に変換し、登録フォームに自動でリクエストを送りメニューを登録する
"""

import requests
import io
import os
import json
import datetime
from bs4 import BeautifulSoup
from pdf2image import convert_from_bytes
from logging import getLogger, FileHandler, INFO


food_dir = os.path.dirname(os.path.abspath(__file__))

# logging
logger = getLogger(__name__)
handler = FileHandler(os.path.join(food_dir, "..", "log/update_menu.log"))
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

# food_url = "http://127.0.0.1:8000"
food_url = "http://35.192.169.248"

school_dormitory_url = "http://ryo.s.toba-cmt.ac.jp/"


def get_html(url):
    # 暁寮のサイトからデータを取得
    res = requests.get(url)
    res.encoding = res.apparent_encoding  # 日本語の文字化けを修正  # https://qiita.com/nittyan/items/d3f49a7699296a58605b
    html = res.text
    return html


def get_menu_pdf_name():
    html = get_html(school_dormitory_url)
    soup = BeautifulSoup(html, "html.parser")
    menu_pdf_name = soup.find("a", text="寮食堂メニュー").get("href")
    return menu_pdf_name


def update_this_month():
    # get url of pdf file of this month menu
    menu_pdf_name = get_menu_pdf_name()

    # download pdf from website
    pdf_res = requests.get(school_dormitory_url + menu_pdf_name)
    # conver pdf to image
    menu_img = convert_from_bytes(pdf_res.content)[0]
    # PIL image to bytes
    img_byte_arr = io.BytesIO()
    menu_img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    # send post request
    logger.info("send POST request to food api")
    requests.post("{}/food/form/".format(food_url), files={"file": img_byte_arr}, timeout=600)
    logger.info("Done request for registration menu")


def read_previous_pdf_name(text_path):
    text = ""
    if os.path.exists(text_path):
        with open(text_path, "r") as f:
            text = f.read()
    else:
        with open(text_path, "w") as f:
            f.write(text)

    return text


# 今月のメニューデータが存在しているか
def exist_this_month_menu():
    now = datetime.datetime.now()
    url = "{}/food/api/{}/{}/".format(food_url, now.year, now.month)
    menu = requests.get(url)
    menu = json.loads(menu.text)
    return bool(menu)


if __name__ == "__main__":
    text_path = os.path.join(food_dir, "pdf_name.txt")

    # 今月のデータが存在してない
    if not exist_this_month_menu():
        # 前のpdfファイル名と現在寮HPにあるPDFの名前を取得
        previous_pdf_name = read_previous_pdf_name(text_path)
        current_pdf_name = get_menu_pdf_name()

        # 寮HP上のPDFが更新されているならメニューを登録
        if current_pdf_name != previous_pdf_name:
            logger.info("Updating Menu Data...")
            update_this_month()
            # write current pdf name on website to txt file
            with open(text_path, "w") as f:
                f.write(current_pdf_name)
            logger.info("Done updating menu data of this month")
        else:
            logger.info("DB doesn't have Menu data of this month, but Akatsuki Dormitory hasn't updated PDF")
            print("寮のWebサイトのPDFはまだ更新されていません")
    else:
        logger.debug("update nothing")
        print("今月のデータは登録済み")
