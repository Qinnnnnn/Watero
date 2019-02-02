#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : push_service.py
Author : Zerui Qin
CreateDate : 2019-02-01 10:00:00
LastModifiedDate : 2019-02-01 10:00:00
Note : WebSocket主动推送服务
"""

import threading

import src.websockets.utils.shared_core as shared_core
from src.websockets.core.exception import ConnMapGetSocketException
from src.websockets.protocol.transmission import Transmission
from utils.log import log_debug


class PushService(threading.Thread):
    """
    WebSocket主动推送服务类，继承自threading.Thread类实现继承式多线程
    """

    def __init__(self, conn_map):
        """
        初始化
        :param conn_map: WebSocket连接映射表
        """
        super(PushService, self).__init__()
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
                popcorn = shared_core.shared_queue.get()  # 共享队列弹出数据
                index = popcorn.index
                msg = popcorn.msg
                try:
                    ws_transmission = Transmission(index=index, conn_map=self.conn_map)
                    ws_transmission.send_frame(msg=msg)
                    log_debug.logger.info('WebSocket {0}: {1} 信息下发成功'.format(index, msg))
                except ConnMapGetSocketException as exp:
                    log_debug.logger.info('WebSocket {0}: {1} 信息下发失败'.format(index, exp.msg))
