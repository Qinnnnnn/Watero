#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : get_config.py
Author : Zerui Qin
CreateDate : 2019-02-26 10:00:00
LastModifiedDate : 2019-02-26 10:00:00
Note : 获取数据库配置
"""
import os

import yaml


def get_config(item):
    work_dir = os.getcwd()
    path = os.path.join(work_dir, 'config', 'identify.yaml')
    with open(path, 'rb') as f:
        return yaml.full_load(f)[item]
