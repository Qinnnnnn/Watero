#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : msg_queue.py
Author : Zerui Qin
CreateDate : 2019-02-01 10:00:00
LastModifiedDate : 2019-02-01 10:00:00
Note : HTTP服务到WebSocket服务的数据实体类
"""

import queue


class PopcornModel:
    def __init__(self, index, msg):
        """
        WebSocket RPC服务到WebSocket服务数据模型
        """
        self.index = index
        self.msg = msg


mq = queue.Queue()
