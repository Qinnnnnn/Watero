#!/usr/bin/env bash

# 启动Gunicorn WebServer
gunicorn -c ./config/gunicorn.conf "flask_manage:create_app()" &
python websocket_manage.py