#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.restfuls.apps import create_app

if __name__ == '__main__':
    flask_server = create_app()  # 实例化Flask
    flask_server.run('0.0.0.0')
