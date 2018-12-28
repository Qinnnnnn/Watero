#!/usr/bin/env bash
# 启动Conda虚拟环境
source activate Watero

# 启动Gunicorn WebServer
gunicorn -c ./config/gunicorn_config.py "manage:create_app()"