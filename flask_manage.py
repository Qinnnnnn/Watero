#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : flask_manage.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : 拉起HTTP服务入口
"""

from src.restfuls.apps import create_app

if __name__ == '__main__':
    flask_server = create_app()  # 实例化HTTP服务
    flask_server.run(host='0.0.0.0', port=5000, debug=False)
