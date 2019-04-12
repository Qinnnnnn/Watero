#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : push_service.py
Author : Zerui Qin
CreateDate : 2019-02-01 10:00:00
LastModifiedDate : 2019-02-01 10:00:00
Note : WebSocket Push服务
"""

import threading

import utils.shared_core as shared_core
from src.websockets.extension.exception import ConnMapGetSocketException
from src.websockets.protocol.transmission import Transmission
from utils.log import log_debug


class PushService(threading.Thread):
    """
    WebSocket Push服务类，继承自threading.Thread类实现继承式多线程
    从共享消息队列中阻塞式获取待推送信息推送至对应的Agent
    """

    def __init__(self, conn_map):
        """
        初始化
        :param conn_map: 连接映射表
        """
        super(PushService, self).__init__()
        self.ws_transmission = Transmission(conn_map=conn_map)

    def run(self):
        """
        线程启动函数
        :return:
        """
        while True:
            popcorn = shared_core.shared_queue.get()  # 阻塞等待队列数据
            index = popcorn.index
            msg = popcorn.msg
            try:
                self.ws_transmission.init_socket(index=index)  # 初始化socket索引号
                self.ws_transmission.send(msg=msg)  # 发送信息
                log_debug.logger.info(f'WebSocket {index}: 信息推送成功')
            except ConnMapGetSocketException:
                log_debug.logger.error(f'WebSocket {index}: 连接不存在')
            except Exception:
                log_debug.logger.error(f'WebSocket {index}: 信息推送失败')
