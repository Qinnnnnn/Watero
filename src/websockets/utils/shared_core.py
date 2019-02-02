#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : shared_core.py
Author : Zerui Qin
CreateDate : 2019-02-01 10:00:00
LastModifiedDate : 2019-02-01 10:00:00
Note : WebSocket RPC服务到WebSocket服务的数据类
"""

import queue


class PopcornModel:
    def __init__(self, index, msg):
        """
        WebSocket RPC服务到WebSocket服务数据模型
        """
        self.index = index
        self.msg = msg


shared_queue = queue.Queue()  # WebSocket RPC服务到WebSocket服务共享队列
