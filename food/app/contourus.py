# 元画像からメニュー表のみをトリミングするプログラム

import numpy as np
import cv2


def transform_by4(img, points):
    """ 4点を指定してトリミングする。 """

    points = sorted(points, key=lambda x: x[1])  # yが小さいもの順に並び替え。
    top = sorted(points[:2], key=lambda x: x[0])  # 前半二つは四角形の上。xで並び替えると左右も分かる。
    bottom = sorted(points[2:], key=lambda x: x[0], reverse=True)  # 後半二つは四角形の下。同じくxで並び替え。
    points = np.array(top + bottom, dtype='float32')  # 分離した二つを再結合。

    width = max(np.sqrt(((points[0][0] - points[2][0]) ** 2) * 2),
                np.sqrt(((points[1][0] - points[3][0]) ** 2) * 2))
    height = max(np.sqrt(((points[0][1] - points[2][1]) ** 2) * 2),
                 np.sqrt(((points[1][1] - points[3][1]) ** 2) * 2))

    dst = np.array([
        np.array([0, 0]),
        np.array([width - 1, 0]),
        np.array([width - 1, height - 1]),
        np.array([0, height - 1]),
    ], np.float32)

    trans = cv2.getPerspectiveTransform(points, dst)  # 変換前の座標と変換後の座標の対応を渡すと、透視変換行列を作ってくれる。
    return cv2.warpPerspective(img, trans, (int(width), int(height)))  # 透視変換行列を使って切り抜く。


# 以下main用関数
def trimming(img_path, save_path):
    im = cv2.imread(img_path)  # 画像読み込み
    lines = im.copy()

    # 輪郭を抽出する
    canny = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    canny = cv2.GaussianBlur(canny, (5, 5), 0)
    canny = cv2.Canny(canny, 50, 100)

    cnts = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]  # 抽出した輪郭に近似する直線（？）を探す。
    cnts.sort(key=cv2.contourArea, reverse=True)  # 面積が大きい順に並べ替える。

    warp = None
    for i, c in enumerate(cnts):
        arclen = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * arclen, True)

        level = 1 - float(i) / len(cnts)  # 面積順に色を付けたかったのでこんなことをしている。
        if len(approx) == 4:
            cv2.drawContours(lines, [approx], -1, (0, 0, 255 * level), 2)
            if warp is None:
                warp = approx.copy()  # 一番面積の大きな四角形をwarpに保存。
        else:
            cv2.drawContours(lines, [approx], -1, (0, 255 * level, 0), 2)

        for pos in approx:
            cv2.circle(lines, tuple(pos[0]), 4, (255 * level, 0, 0))

    # cv2.imshow('edge', lines)

    if warp is not None:
        warped = transform_by4(im, warp[:, 0, :])  # warpが存在した場合、そこだけくり抜いたものを作る。
        # cv2.imshow('warp', warped)
        cv2.imwrite(save_path, warped)

if __name__ == '__main__':
    img_path = "image/akatsuki2018_02.jpg"
    save_path = "image/akatsuki2018_02_trimming.jpg"
    trimming(img_path,save_path)