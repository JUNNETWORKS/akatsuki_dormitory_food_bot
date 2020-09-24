import datetime
import json
import os

import requests
import tweepy

CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN_KEY"]
ACCESS_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# メニューデータ取得
now = datetime.datetime.now()
url = "http://35.192.169.248/food/api/{}/{}/{}".format(now.year, now.month, now.day)
menu = requests.get(url)
menu = json.loads(menu.text)

if not menu:  # リストが空の場合
    pass
elif 0 <= now.hour < 8:
    text = "{}月{}日の朝食は、{}です。".format(now.month, now.day, menu[0]["breakfast"])
    api.update_status(text)
elif 8 < now.hour <= 12:
    text = "{}月{}日の昼食は、{}です。".format(now.month, now.day, menu[0]["lunch"])
    api.update_status(text)
else:
    text = "{}月{}日の夕食は、{}です。".format(now.month, now.day, menu[0]["dinner"])
    api.update_status(text)
