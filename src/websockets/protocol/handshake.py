#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : handshake.py
Author : Clever Moon
CreateDate : 2018-12-27 10:00:00
LastModifiedDate : 2018-12-27 10:00:00
Note : WebSocket协议握手类
参阅RFC 6455文档第4部分：http://tools.ietf.org/html/rfc6455#section-4
"""
import base64
import hashlib

from src.websockets.extension.exception import HeaderFormatException, HeaderFieldException, HeaderFieldMultiException
from src.websockets.protocol.transmission import Transmission


class Handshake:
    """
    WebSocket协议握手类
    """

    def __init__(self, index, conn_map):
        """
        初始化
        :param index: int/str - Socket索引号
        :param conn_map: dict - WebSocket连接映射表
        """
        self.index = index
        self.conn_map = conn_map
        self.ws_transmission = Transmission(conn_map=self.conn_map)
        self.GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'  # Magic value
        self.upgrade = ''
        self.connection = ''
        self.key = ''
        self.version = ''

        # noinspection PyMethodMayBeStatic

    def handshake_check(self, msg):
        """
        检查WebSocket握手请求
        :param msg: str - WebSocket握手请求
        :return:
        """
        header_dict = dict()
        if msg.find('\r\n\r\n') == -1:  # 不存在\r\n\r\n分割符号
            raise HeaderFormatException()
        else:
            header, payload_data = msg.split('\r\n\r\n', 1)
            for item in header.split('\r\n')[1:]:  # 丢弃HTTP请求header域第一行数据
                key, value = item.split(': ', 1)  # 逐行解析request header信息
                if key not in header_dict.keys():  # 字段未重复
                    header_dict[key] = value
                else:  # 字段重复
                    raise HeaderFieldMultiException(key)

            self.upgrade = header_dict.get('Upgrade').lower()
            self.connection = header_dict.get('Connection').lower()
            self.key = header_dict.get('Sec-WebSocket-Key')
            self.version = header_dict.get('Sec-WebSocket-Version')

            if self.upgrade is None:  # Upgrade字段不存在
                raise HeaderFieldException('Upgrade', '字段缺失')
            elif self.upgrade == '':  # Upgrade字段为空
                raise HeaderFieldException('Upgrade', '字段为空')
            elif self.upgrade != 'websocket':  # Upgrade字段值不等于websocket
                raise HeaderFieldException('Upgrade', '值错误')

            if self.connection is None:  # Connection字段不存在
                raise HeaderFieldException('Sec-WebSocket-Version', '字段缺失')
            elif self.connection == '':  # Connection字段为空
                raise HeaderFieldException('Sec-WebSocket-Version', '字段为空')
            elif self.connection != 'upgrade':  # Connection字段值不等于Upgrade
                raise HeaderFieldException('Sec-WebSocket-Version', '值错误')

            if self.key is None:  # Sec-WebSocket-Key字段缺失
                raise HeaderFieldException('Sec-WebSocket-Key', '字段缺失')
            elif self.key == '':  # Sec-WebSocket-Key字段为空
                raise HeaderFieldException('Sec-WebSocket-Key', '字段为空')

            if self.version is None:  # Sec-WebSocket-Version字段不存在
                raise HeaderFieldException('Sec-WebSocket-Version', '字段缺失')
            elif self.version == '':  # Sec-WebSocket-Version字段为空
                raise HeaderFieldException('Sec-WebSocket-Version', '字段为空')
            elif self.version != '13':  # Sec-WebSocket-Version字段值不等于13
                raise HeaderFieldException('Sec-WebSocket-Version', '值错误')

    def handshake_response(self):
        """
        发送WebSocket握手响应
        :return:
        """
        response_buffer = self._build_response().encode('utf-8')  # 构造服务端握手响应报文
        self.ws_transmission.init_socket(index=self.index)
        self.ws_transmission.conn.send(response_buffer)

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
