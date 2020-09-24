# 暁寮寮食メニューがデータフレームを返す
import os
import re
import time

import pandas as pd

from .CloudVisionApi_TextDetection import text_detection
from .contourus import trimming
from .split_date_menu import split_img


def Menu_data(img_path, save_path, dir_path):
    trimming(img_path, save_path)  # トリミング
    split_img(save_path, dir_path)  # 分割
    API_KEY = os.environ.get("GOOGLE_API_KEY")

    menu = {"Breakfast": [], "Lunch": [], "Dinner": []}

    files = sorted(os.listdir(dir_path))
    for file in files:
        time.sleep(0.5)

        print("processing: " + str(file), end=": ")

        file_path = dir_path + file
        res_json = text_detection(file_path, API_KEY)

        file_name = os.path.splitext(file)[0]  # ファイル名から拡張子を取り除く ex: menu_1_1
        if "textAnnotations" not in res_json["responses"][0]:
            if file_name[-1] == "1":
                menu["Breakfast"].append(" ")
            elif file_name[-1] == "2":
                menu["Lunch"].append(" ")
            else:
                menu["Dinner"].append(" ")
            continue

        text = res_json["responses"][0]["textAnnotations"][0]["description"]
        text = re.findall(r"[ぁ-んァ-ン一-龠ー]+", text)  # 正規表現を使い日本語を抽出
        text = " ".join(text)  # すべての文字を連結

        print(text, end="\n")

        if file_name[-1] == "1":
            menu["Breakfast"].append(text)
        elif file_name[-1] == "2":
            menu["Lunch"].append(text)
        else:
            menu["Dinner"].append(text)

    menu_df = pd.DataFrame.from_dict(menu)  # データフレームを作成
    menu_df = menu_df.ix[:, ['Breakfast', 'Lunch', 'Dinner']]  # 並び替え

    return menu_df


if __name__ == '__main__':
    img_path = "food/static/image/akatsuki2018_01.jpg"
    save_path = "food/static/image/akatsuki_menu.jpg"
    dir_path = "food/static/image/split_img"

    data = Menu_data(img_path, save_path, dir_path)
    print(data)
