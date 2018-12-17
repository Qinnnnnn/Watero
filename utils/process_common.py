#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : process_common.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
LastModifiedDate : 2018-12-07 10:00:00
Note : 进程间通信公共组件
"""

from multiprocessing import Manager
from multiprocessing import Pipe
from multiprocessing import Queue

websocket_share_dict = Manager().dict()  # WebSocket 共享字典
share_list = Manager().list()  # 共享列表
share_queue = Queue()  # 共享队列
share_pipe_parent, share_pipe_child = Pipe()  # 共享管道
