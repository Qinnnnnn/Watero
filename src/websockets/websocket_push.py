#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : websocket_push.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket主动推送服务类
"""

import threading

import src.websockets.utils.shared_core as shared_core
from src.websockets.core.exception import ConnMapGetSocketException
from src.websockets.protocol.transmission import Transmission
from utils.log import log_debug


class WebSocketPush(threading.Thread):
    """
    WebSocket主动推送服务，继承自threading.Thread类实现继承式多线程
    """

    def __init__(self, conn_map):
        """
        初始化
        :param conn_map: WebSocket连接映射表
        """
        # 初始化线程
        super(WebSocketPush, self).__init__()
        # 初始化数据
        self.conn_map = conn_map

    def run(self):
        """
        线程启动函数
        :return:
        """
        log_debug.logger.info('WebSocket主动推送服务启动')
        while True:  # 循环读取共享队列中的数据
            if shared_core.shared_queue.empty():  # 不存在数据
                pass
            else:  # 存在数据
                popcorn = shared_core.shared_queue.get()
                try:
                    ws_transmission = Transmission(index=popcorn.index, conn_map=self.conn_map)
                    ws_transmission.send_frame(msg=popcorn.msg)
                    log_debug.logger.info('WebSocket {0}: {1} 信息下发成功'.format(popcorn.index, popcorn.msg))
                except ConnMapGetSocketException as exp:
                    log_debug.logger.info('WebSocket {0}: {1} 信息下发失败'.format(popcorn.index, exp.msg))
