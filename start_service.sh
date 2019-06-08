#!/usr/bin/env bash
gunicorn -c ./config/gunicorn.py "flask_manage:create_app()" &
python websocket_manage.py