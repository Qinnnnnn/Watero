#!/usr/bin/env bash

# 启动Gunicorn Web Server
gunicorn -c ./config/gunicorn.py "flask_manage:create_app()" &
python websocket_manage.py