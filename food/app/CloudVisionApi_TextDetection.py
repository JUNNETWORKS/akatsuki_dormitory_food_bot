import base64  # httpリクエストのためにエンコードする
import json
import os

import requests

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
API_KEY = os.environ.get("GOOGLE_API_KEY")


def text_detection(image_path, API_KEY):
    api_url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(API_KEY)
    with open(image_path, "rb") as img:
        image_content = base64.b64encode(img.read())
        req_body = json.dumps({
            'requests': [{
                'image': {
                    'content': image_content.decode('utf-8')  # jsonにするためにバイト列から文字列にする
                },
                'features': [{
                    'type': 'TEXT_DETECTION'
                }]
            }]
        })
        res = requests.post(api_url, data=req_body)
        return res.json()


if __name__ == "__main__":
    img_path = "image/split_img/menu_25_3.jpg"
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    res_json = text_detection(img_path, API_KEY)
    res_text = res_json["responses"][0]["textAnnotations"][0]["description"]
    # print(json.dumps(res_json, indent=4, sort_keys=True,
    # ensure_ascii=False))   # ensure_ascii=False で日本語文字化けを防ぐ
    print(res_text)
    with open("test2.json", "w") as js:
        # json.dump(res_json, js, indent=4, ensure_ascii=False)
        js.write(res_text)
