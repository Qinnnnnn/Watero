#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : connection.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket连接被动响应线程
"""

import threading

from src.websockets.extension.exception import HeaderFormatException, HeaderFieldMultiException, HeaderFieldException, \
    SocketCloseAbnormalException
from src.websockets.protocol.handshake import Handshake
from src.websockets.protocol.transmission import Transmission
from utils.log import log_debug


class Connection(threading.Thread):
    """
    WebSocket连接对象, 继承自threading.Thread类实现继承式多线程
    """

    def __init__(self, conn_map, index, conn, host, remote, debug=False):
        """
        初始化
        :param conn_map: 连接映射表
        :param index: WebSocket连接对应的socket索引号
        :param conn: WebSocket连接对应的socket句柄
        :param host: WebSocket连接对应的的远程主机地址
        :param remote: WebSocket连接对应的远程主机地址 + 端口号
        :param debug: 是否为调试模式
        """
        # 初始化线程
        super(Connection, self).__init__()
        # 初始化数据
        self.conn_map = conn_map
        self.index = index
        self.conn = conn
        self.host = host
        self.remote = remote
        self.debug = debug

        self.is_handshake = False  # WebSocket连接是否握手
        self.is_online = False  # WebSocket连接是否响应PING心跳包
        self.recv_buffer = b''  # 接收到的字节序列
        self.recv_buffer_str = ''  # 接收到的字符串
        self.recv_buffer_length = 0  # 接收到的字节序列长度
        self.frame_header_length = 0  # 数据帧头部长度
        self.frame_payload_length = 0  # 数据帧有效载荷长度

    def run(self):
        """
        线程启动函数
        :return:
        """
        ws_handshake = Handshake(self.index, self.conn_map)
        ws_transmission = Transmission(self.conn_map)
        ws_transmission.init_socket(index=self.index)

        while True:  # 循环接收WebSocket Client消息
            if self.is_handshake is False:  # WebSocket未建立连接
                self.recv_buffer += self.conn.recv(1024)  # 接收字节序列，可能存在一次性不能接受完header的情况
                self.recv_buffer_str = self.recv_buffer.decode('utf-8')  # 字节序列解码
                try:
                    ws_handshake.handshake_check(self.recv_buffer_str)  # 检查WebSocket握手请求
                except HeaderFormatException as exp:
                    log_debug.logger.error(f'WebSocket {self.index}: {exp.msg}')
                    continue  # 未检查到\r\n\r\n则跳过本次循环继续接收
                except (HeaderFieldMultiException, HeaderFieldException) as exp:
                    ws_transmission.remove_conn()  # WebSocket连接建立失败，删除连接映射表中的当前socket句柄
                    log_debug.logger.error(f'WebSocket {self.index}: {exp.msg}')

                ws_handshake.handshake_response()  # 发送WebSocket握手响应
                log_debug.logger.info(f'WebSocket {self.index}: 握手成功')

                self.is_online = ws_transmission.heartbeat()  # 心跳测试
                if self.is_online is True:
                    self.is_handshake = True  # WebSocket 连接成功建立，修改握手标志
                    log_debug.logger.info(f'WebSocket {self.index}: 建立连接')
                else:
                    ws_transmission.remove_conn()  # WebSocket连接建立失败，删除连接映射表中的当前socket句柄
                self.recv_buffer_str = ''
            else:  # WebSocket已建立连接，响应控制帧
                try:
                    field_list = ws_transmission.recv()
                    if field_list:
                        self.recv_buffer = field_list[-1]
                        flag = ws_transmission.passive_respond(field_list)  # 响应控制帧
                        if flag:
                            log_debug.logger.info(f'WebSocket {self.index}: opcode {field_list[4]} 控制帧已响应')
                        else:
                            log_debug.logger.error(f'WebSocket {self.index}: opcode {field_list[4]} 数据帧未响应')
                    else:
                        log_debug.logger.info(f'WebSocket {self.index} 数据帧解析失败')
                except SocketCloseAbnormalException as exp:  # WebSocket 异常关闭
                    ws_transmission.remove_conn()  # 从连接映射表中删除句柄
                    log_debug.logger.error(f'WebSocket {self.index}: {exp.msg}')

                self.recv_buffer = b''
                self.recv_buffer_str = ''
                self.recv_buffer_length = 0
                self.frame_header_length = 0
                self.frame_payload_length = 0

            if self.conn_map.get(str(self.index)) is None:  # 连接映射表中已不存socket句柄
                log_debug.logger.info(f'WebSocket {self.index}: 连接释放')
                break
