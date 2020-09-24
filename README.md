# 暁寮寮食 BOT

[Twitter](https://twitter.com/Toba_Akatsuki)

## systemd

`/etc/systemd/system/akatsuki.service`

```systemd
[Unit]
Description=gunicorn daemon for akatsuki
After=network.target

[Service]
User=webapp
Group=www-data
WorkingDirectory=/home/webapp/akatsuki
ExecStart=/home/webapp/.local/share/virtualenvs/akatsuki-EDsZsOmf/bin/gunicorn --workers 1 --access-logfile - --timeout 600 --bind unix:/home/webapp/akatsuki/akatsuki.sock --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Nginx

`akatsuki-nginx.conf` のシンボリックリンクを `/etc/nginx/sites-enabled/` に貼りましょう.

## cron

以下の処理を自動的に行うために crontab を設定します

- ツイート
- メニュー表が更新されたかどうかの確認
