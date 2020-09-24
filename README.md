# 暁寮寮食 BOT

鳥羽商船高等専門学校-暁寮の寮食メニューを定期的にツイートする BOT です.

[Twitter](https://twitter.com/Toba_Akatsuki)

[サイト](https://t.co/CNUt7w3Bz4?amp=1)

[作った経緯などについて](https://jun-networks.hatenablog.com/entry/2018/03/04/020843)

## 動かし方

### 環境変数設定

`.env` ファイルに以下の様にシークレットキーなどの情報を載せる

```conf
# Twitter
CONSUMER_KEY=<Twitter_CONSUMER_KEY>
CONSUMER_SECRET=<Twitter_CONSUMER_SECRET>
ACCESS_TOKEN_KEY=<Twitter_ACCESS_TOKEN_KEY>
ACCESS_TOKEN_SECRET=<Twitter_ACCESS_TOKEN_SECRET>

# Google API
GOOGLE_API_KEY=<GOOGLE_API_KEY>

# Django
DJANGO_SECRET_KEY=<DJANGO_SECRET_KEY>
```

### Pipenv

```bash
pipenv install
```

で依存ライブラリをインストールする.

### DB Migration

```bash
pipenv run python manage.py migrate
```

で DB(sqlite)にテーブル作成

### systemd

`/etc/systemd/system/akatsuki.service` に以下の内容を書き込む.

```systemd
[Unit]
Description=gunicorn daemon for akatsuki
After=network.target

[Service]
User=webapp
Group=www-data
WorkingDirectory=/home/webapp/akatsuki
ExecStart=/home/webapp/.local/bin/pipenv run gunicorn --workers 1 --access-logfile - --timeout 600 --bind unix:/home/webapp/akatsuki/akatsuki.sock --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application

[Install]
WantedBy=multi-user.target
```

pipenv のパスとかは適当に変えてください.

### Nginx

`akatsuki-nginx.conf` のシンボリックリンクを `/etc/nginx/sites-enabled/` に貼りましょう.

```bash
ln -s /home/webapp/akatsuki/akatsuki-nginx.conf /etc/nginx/sites-enabled/akatsuki
```

### cron

以下の処理を自動的に行うために crontab を設定します

- ツイート
- メニュー表が更新されたかどうかの確認

```cron
0 0 */1 * * python3 /home/webapp/akatsuki/food/update_menu.py
0 7 * * * export $(cat /home/webapp/akatsuki/.env | grep -v ^# | xargs); python3 /home/webapp/akatsuki/tweet_sender.py
0 11 * * * export $(cat /home/webapp/akatsuki/.env | grep -v ^# | xargs); python3 /home/webapp/akatsuki/tweet_sender.py
0 17 * * * export $(cat /home/webapp/akatsuki/.env | grep -v ^# | xargs); python3 /home/webapp/akatsuki/tweet_sender.py
```

`export $(cat /home/webapp/akatsuki/.env | grep -v ^# | xargs);` のところでシークレットキーなどの値を読み込んでいる
