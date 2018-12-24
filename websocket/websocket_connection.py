#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : websocket_connection.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket建立连接后的连接对象
"""

import threading

from utils.log import log_debug
from websocket.websocket_common import WebSocketHandshakeUtil
from websocket.websocket_common import WebSocketProtocolUtil


class WebSocketConnection(threading.Thread):
    """
    定义WebSocket连接对象, 继承自threading.Thread类实现继承式多线程
    """

    def __init__(self, conn_map, index, conn, host, remote, debug=False):
        """
        初始化
        :param conn_map: 连接映射
        :param index: 当前WebSocket连接的socket标识
        :param conn: 当前WebSocket的socket句柄
        :param host: 当前WebSocket连接的远程主机地址
        :param remote: 当前WebSocket连接的远程主机地址+端口号
        :param debug: 是否为调试模式
        """
        # 初始化线程
        super(WebSocketConnection, self).__init__()
        # 初始化数据
        self.conn_map = conn_map
        self.conn = conn
        self.index = index
        self.host = host
        self.remote = remote
        self.debug = debug

        self.is_handshake = False  # WebSocket连接是否握手的标志, 初始化为False
        self.is_online = False  # WebSocket连接是否在线
        self.recv_buffer = b''  # 保存接收到的字节序列
        self.recv_buffer_str = ''  # 保存接收到的字节序列转str
        self.recv_buffer_length = 0  # 保存接收到的字节序列长度
        self.frame_header_length = 0  # 保存数据帧头部长度
        self.frame_payload_length = 0  # 保存数据帧有效载荷长度

    def run(self):
        """
        线程启动
        :return:
        """
        wpu = WebSocketProtocolUtil(self.index, self.conn_map)
        whu = WebSocketHandshakeUtil(self.index, self.conn_map)
        while True:  # 循环接收WebSocket Client信息
            if self.is_handshake is False:  # WebSocket未建立连接，响应握手请求
                self.recv_buffer_str = self.conn.recv(1024).decode('utf-8')  # 接收1024字节数据, 并解码为Unicode字符串
                status = whu.parse_handshake_request(self.recv_buffer_str)
                if status == 0:  # WebSocket握手请求解析成功
                    whu.respond_handshake_request()
                    self.is_online = wpu.heartbeat()
                    if self.is_online is True:  # WebSocket Client响应心跳成功
                        self.is_handshake = True  # WebSocket 连接成功建立之后修改握手标志
                    else:  # WebSocket Client响应心跳失败
                        wpu.remove_conn()
                        break
                else:  # WebSocket握手请求解析失败
                    wpu.remove_conn()
                    break
                self.recv_buffer_str = ''
            else:  # WebSocket已建立连接，响应控制帧
                log_debug.logger.info('WebSocket {0} 已连接'.format(self.host))
                self.recv_buffer = wpu.recv_buffer()
                if self.recv_buffer:  # 数据不为空
                    frame_tuple = WebSocketProtocolUtil.bytify_buffer(self.recv_buffer)  # 解析数据帧字节序列
                    opcode = wpu.respond_control_frame(frame_tuple)  # 响应控制帧
                    if opcode != 0:
                        log_debug.logger.error('WebSocket {0} {1}号控制帧已响应'.format(self.index, opcode))
                    else:
                        pass
                else:  # 数据帧为空, WebSocket 异常关闭
                    wpu.remove_conn()  # 从 WebSocket 连接映射表中删除句柄
                    break
                self.recv_buffer = b''
                self.recv_buffer_str = ''
                self.recv_buffer_length = 0
                self.frame_header_length = 0
                self.frame_payload_length = 0
