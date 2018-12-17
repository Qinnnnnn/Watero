#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : websocket_conn.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket建立连接后的连接对象
"""

import threading

from utils.log import log_debug
from websocket.websocket_util import WebSocketHandshakeUtil
from websocket.websocket_util import WebSocketProtocolUtil


class WebSocket(threading.Thread):
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
        super(WebSocket, self).__init__()
        # 初始化数据
        self.conn_map = conn_map
        self.conn = conn
        self.index = index
        self.host = host
        self.remote = remote
        self.debug = debug

        self.is_handshake = False  # WebSocket 连接是否握手的标志, 初始化为False
        self.is_online = False  # WebSocket 连接是否在线
        self.recv_buffer = b''  # 保存接收到的字节序列
        self.recv_buffer_str = ''  # 保存接收到的字节序列转str
        self.recv_buffer_length = 0  # 保存接收到的字节序列长度
        self.frame_header_length = 0  # 保存数据帧头部长度
        self.frame_payload_length = 0  # 保存数据帧有效载荷长度

    def run(self):
        """
        运行线程
        :return:
        """
        log_debug.logger.info('WebSocket {0} 启动'.format(self.host))
        while True:  # 循环接收 WebSocket Client 信息
            if self.is_handshake is False:  # WebSocket 未建立连接
                # TODO 此处需要判断是否已经获取握手请求的全部信息
                self.recv_buffer_str = self.conn.recv(1024).decode('utf-8')  # 每次接收1024个字节, 并解码为 Unicode 字符串
                header_dict = WebSocketHandshakeUtil.parse_handshake_request(self.recv_buffer_str)
                if header_dict:  # WebSocket握手请求解析成功
                    log_debug.logger.info('WebSocket {0} 握手解析成功'.format(self.index))
                    WebSocketHandshakeUtil.respond_handshake_request(header_dict, self.index, self.conn_map)
                    self.is_online = WebSocketProtocolUtil.heartbeat(self.index, self.conn_map)
                    if self.is_online is True:  # 心跳连接成功
                        log_debug.logger.info('WebSocket {0} 连接建立成功'.format(self.index))
                        self.is_handshake = True  # WebSocket 连接成功建立之后修改握手标志
                        self.recv_buffer_str = ''
                    else:  # 心跳连接失败
                        log_debug.logger.info('WebSocket {0} 连接建立失败'.format(self.index))
                        WebSocketProtocolUtil.remove_conn(self.index, self.conn_map)
                        break
                else:  # WebSocket握手请求解析失败
                    log_debug.logger.error('WebSocket {0} 握手解析失败'.format(self.index))
                    WebSocketProtocolUtil.remove_conn(self.index, self.conn_map)
                    break
            else:  # WebSocket 已建立连接
                self.recv_buffer = WebSocketProtocolUtil.recv_frame(self.index, self.conn_map)
                if self.recv_buffer:  # 数据帧不为空
                    frame_tuple = WebSocketProtocolUtil.bytify_buffer(self.recv_buffer)  # 解析数据帧字节序列
                    rt_tuple = WebSocketProtocolUtil.respond_frame(frame_tuple, self.index, self.conn_map)  # 响应数据帧
                    if rt_tuple[0] == 1 and rt_tuple[1]:  # opcode 为1并且client_mac_addr不为空
                        client_mac_addr = rt_tuple[1]
                        self.conn_map[client_mac_addr] = self.conn_map.pop(self.index)  # # WebSocket Client 连接映射表
                        self.index = client_mac_addr  # 更新索引号
                    elif rt_tuple[0] == 8:
                        WebSocketProtocolUtil.remove_conn(self.index, self.conn_map)  # 从 WebSocket 连接映射表中删除句柄
                        log_debug.logger.info('WebSocket {0} 断开'.format(self.index))
                    else:  # opcode 为其他值或client_mac_addr为空暂不做处理
                        pass
                    self.recv_buffer = b''
                    self.recv_buffer_str = ''
                    self.recv_buffer_length = 0
                    self.frame_header_length = 0
                    self.frame_payload_length = 0
                else:  # 数据帧为空, WebSocket 异常关闭
                    WebSocketProtocolUtil.remove_conn(self.index, self.conn_map)  # 从 WebSocket 连接映射表中删除句柄
                    break
