#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : handshake.py
Author : Clever Moon
CreateDate : 2018-12-27 10:00:00
LastModifiedDate : 2018-12-27 10:00:00
Note : 处理WebSocket协议握手部分
参阅RFC 6455文档第4部分：http://tools.ietf.org/html/rfc6455#section-4
"""
import base64
import hashlib

from src.websockets.exception import HeaderFormatException, HeaderFieldException, HeaderFieldMultiException
from src.websockets.protocol import WebSocketProtocol
from utils.log import log_debug


class WebSocketHandshake:
    """
    WebSocket协议握手请求类
    """

    def __init__(self, index, conn_map):
        """
        初始化
        :param index: int/str - Socket索引号
        :param conn_map: dictproxy - WebSocket Client连接映射表
        """
        self.index = index
        self.conn_map = conn_map

        self.GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'  # Magic value
        self.header_dict = dict()
        self.key = ''
        self.upgrade = ''
        self.version = ''

    def _accept_request(self, key):
        """
        接受握手请求，计算握手响应中的Sec-Websocket-Accept字段
        :param key: WebSocket握手请求中Sec-WebSocket-Key字段
        :return: bytes - Sec_Websocket_Accept值
        """
        sha1 = hashlib.sha1((key + self.GUID).encode('utf-8')).digest()
        return base64.b64encode(sha1).decode()

    def _build_response(self):
        """
        构建WebSocket握手响应
        :return:
        """
        sec_websocket_accept = self._accept_request(self.key)
        response = 'HTTP/1.1 101 Switching Protocols\r\n' \
                   'Connection: Upgrade\r\n' \
                   'Upgrade: websocket\r\n' \
                   'Sec-WebSocket-Accept: ' + sec_websocket_accept + '\r\n\r\n'
        return response

    def handshake_request_check(self, msg):
        """
        检查WebSocket握手请求
        :param msg: str - WebSocket握手请求
        :return:
        """
        if msg.find('\r\n\r\n') == -1:  # 不存在\r\n\r\n分割符号
            raise HeaderFormatException()
        else:
            header, payload_data = msg.split('\r\n\r\n', 1)
            for item in header.split('\r\n')[1:]:  # 丢弃HTTP请求header域第一行数据
                key, value = item.split(': ', 1)  # 逐行解析request header信息
                if key not in self.header_dict.keys():  # 字段未重复
                    self.header_dict[key] = value
                else:  # 字段重复
                    raise HeaderFieldMultiException(key)

            self.key = self.header_dict.get('Sec-WebSocket-Key')
            self.version = self.header_dict.get('Sec-WebSocket-Version')
            self.upgrade = self.header_dict.get('Upgrade')

            if self.key is None:  # Sec-WebSocket-Key字段缺失
                raise HeaderFieldException('Sec-WebSocket-Key', '字段缺失')
            elif self.key == '':  # Sec-WebSocket-Key字段为空
                raise HeaderFieldException('Sec-WebSocket-Key', '字段为空')

            if self.version is None:  # Sec-WebSocket-Version字段不存在
                raise HeaderFieldException('Sec-WebSocket-Version', '字段缺失')
            elif self.version == '':  # Sec-WebSocket-Version字段为空
                raise HeaderFieldException('Sec-WebSocket-Version', '字段为空')
            elif self.version != '13':  # Sec-WebSocket-Version字段值不等于13
                raise HeaderFieldException('Sec-WebSocket-Version', '版本错误')

    def handshake_response(self):
        """
        发送WebSocket握手响应
        :return:
        """
        ws_protocol = WebSocketProtocol(self.index, self.conn_map)
        response = self._build_response()
        response_buffer = response.encode('utf-8')
        ws_protocol.conn.send(response_buffer)
