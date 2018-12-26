#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : gunicorn_config.py
Author : Zerui Qin
CreateDate : 2018-12-26 10:00:00
LastModifiedDate : 2018-12-26 10:00:00
Note : Gunicorn服务器配置
"""
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 300
