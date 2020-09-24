import cv2
from tqdm import tqdm


def split_img(img_path, dir_path):
    img = cv2.imread(img_path)
    height, width, channels = img.shape

    height_split = 32
    width_split = 12
    new_img_height = int(height / height_split)
    new_img_width = int(width/width_split)

    width_end = 0
    for h in tqdm(range(height_split), desc="split images"):
        height_start = h * new_img_height
        height_end = height_start + new_img_height
        if h == 0: continue # 最上部の情報は不要なため
        for w in range(5):
            width_start = width_end
            if w == 0:  # 日付曜日
                width_end = new_img_width
                continue    # 日付はインデックスで判断するため不要
            elif w == 1: width_end = new_img_width * 3  # 朝
            elif w == 2: width_end = new_img_width * 6  # 昼
            elif w == 3: width_end = new_img_width * 10  # 晩
            else:  # カロリー情報などの不要部分の処理
                width_end=0  # 次の行用に0に戻しておく
                continue
            h_format = "{0:02d}".format(h)  # ２桁に桁あわせする ex: 1=>"01", 20=>"20"  # str型が返ってくる
            file_name = dir_path + "menu_" + h_format + "_" + str(w) + ".jpg"
            clp = img[height_start:height_end, width_start:width_end]
            cv2.imwrite(file_name, clp)


if __name__ == '__main__':
    img_path = "image/akatsuki2018_01_trimming.jpg"
    dir_path = "image/split_img/"

    split_img(img_path, dir_path)
