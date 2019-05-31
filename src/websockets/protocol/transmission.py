#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : transmission.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket协议数据传输类
WebSocket协议数据帧格式
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-------+-+-------------+-------------------------------+
 |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
 |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
 |N|V|V|V|       |S|             |   (if payload len==126/127)   |
 | |1|2|3|       |K|             |                               |
 +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
 |     Extended payload length continued, if payload len == 127  |
 + - - - - - - - - - - - - - - - +-------------------------------+
 |                               |Masking-key, if MASK set to 1  |
 +-------------------------------+-------------------------------+
 | Masking-key (continued)       |          Payload Data         |
 +-------------------------------- - - - - - - - - - - - - - - - +
 :                     Payload Data continued ...                :
 + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
 |                     Payload Data continued ...                |
 +---------------------------------------------------------------+
"""

import struct
import time

import six

from src.websockets.extension.mapping import OPCODE, CLOSE_CODE
from src.websockets.extension.exception import SocketCloseAbnormalException, ConnMapGetSocketException
from utils.log import log_debug


class Transmission:
    """
    WebSocket协议数据传输类
    """

    def __init__(self, conn_map):
        """
        初始化
        :param conn_map: dict - WebSocket连接映射表
        """
        self.index = ''
        self.conn_map = conn_map
        self.conn = None

    def init_socket(self, index):
        """
        初始化socket句柄
        :param index: str - Socket索引号
        :return:
        """
        self.index = index
        self.conn = self._get_socket_handle()

    def send(self, msg, fin='1', rsv1='0', rsv2='0', rsv3='0', opcode='0001'):
        """
        WebSocket数据帧发送函数，可指定数据帧第一个字节的字段值
        :param msg: str - 待发送消息
        :param fin: str - FIN字段
        :param rsv1: str - RSV1字段
        :param rsv2: str - RSV2字段
        :param rsv3: str - RSV3字段
        :param opcode: str - Opcode字段
        :return:
        """
        msg_buffer = msg.encode('utf-8')  # 消息字节序列
        msg_length = len(msg_buffer)  # 消息字节序列长度

        if msg_length <= (2 ** 64 - 1):  # 消息无需分片
            stream = struct.pack('B', int(fin + rsv1 + rsv2 + rsv3 + opcode, 2))  # 默认10000001编码头部第一个字节

            if msg_length <= 125:  # 当消息内容长度<=125时, 数据帧第2个字节低7位直接标示消息内容的长度
                stream += struct.pack('B', msg_length)
                stream += msg_buffer
            elif msg_length <= 2 ** 16 - 1:  # 当消息内容长度需要2个字节来表示时, 此字节低7位取值为126, 由后2个字节标示信息内容的长度
                stream += struct.pack('B', 126)
                stream += struct.pack('>H', msg_length)  # 以网络序编码为unsigned short(2 bytes)的结构体
                stream += msg_buffer
            else:  # 当消息内容长度需要8个字节来表示时，此字节低7位取值为127，由后8个字节标示信息内容的长度
                stream += struct.pack('B', 127)
                stream += struct.pack('>Q', msg_length)  # 以网络序编码为unsigned long long(8 bytes)结构体
                stream += msg_buffer
        else:  # 消息需要分片
            stream = struct.pack('B', int(fin + rsv1 + rsv2 + rsv3 + opcode, 2))
            stream += struct.pack('B', 127)
            stream += struct.pack('>Q', 2 ** 64 - 1)  # 以网络序编码为unsigned long long(8 bytes)结构体
            stream += msg_buffer[0:2 ** 64]
            msg_buffer = msg_buffer[2 ** 64:]  # 重新截取消息字节序列
            msg_length = len(msg_buffer)  # 重新计算消息字节序列长度

            # 数据分片延续帧
            while msg_length > (2 ** 64 - 1):
                fin = '0'
                opcode = '0000'
                stream += struct.pack('B', int(fin + rsv1 + rsv2 + rsv3 + opcode, 2))
                stream += struct.pack('B', 127)
                stream += struct.pack('>Q', 2 ** 64 - 1)  # 以网络序编码为unsigned long long(8 bytes)结构体
                stream += msg_buffer[0:2 ** 64]
                msg_buffer = msg_buffer[2 ** 64:]  # 重新截取消息字节序列
                msg_length = len(msg_buffer)  # 计算消息字节序列长度

            stream = struct.pack('B', int(fin + rsv1 + rsv2 + rsv3 + opcode, 2))
            if msg_length <= 125:  # 当消息内容长度小于等于125时，数据帧的第2个字节低7位直接标示消息内容的长度
                stream += struct.pack('B', msg_length)
            elif msg_length <= 65535:  # 当消息内容长度需要2个字节来表示时，此字节低7位取值为126，由后2个字节标示信息内容的长度
                stream += struct.pack('B', 126)
                stream += struct.pack('>H', msg_length)  # 以网络序编码为unsigned short(2 bytes)的结构体
            else:  # 当消息内容长度需要8个字节来表示时，此字节低7位取值为127，由后8个字节标示信息内容的长度
                stream += struct.pack('B', 127)
                stream += struct.pack('>Q', msg_length)  # 以网络序编码为unsigned long long(8 bytes)结构体
        self.conn.send(stream)

    def recv(self):
        """
        WebSocket数据帧接收函数
        :return: list - 解析后的数据帧
        """
        recv_buffer = b''
        while True:
            recv_buffer += self.conn.recv(1024)
            if len(recv_buffer) == 0:  # Socket异常关闭
                raise SocketCloseAbnormalException()  # 抛出Socket异常关闭的异常
            else:  # Socket正常接收数据
                field_list = self._bytify_buffer(buffer=recv_buffer)  # 解析数据帧字节序列
                if field_list:
                    if field_list[0] == 0:  # FIN字段为0
                        # TODO 接收WebSocket数据延续帧
                        pass
                    elif field_list[0] == 1:  # FIN字段为1
                        real_buffer_length = self._calc_length(recv_buffer)
                        recv_buffer_length = len(recv_buffer)
                        if recv_buffer_length < real_buffer_length:  # 数据帧未接收完整
                            continue
                        else:  # 数据帧接收完整
                            return field_list
                else:
                    return None

    def passive_respond(self, field_list):
        """
        被动响应WebSocket控制帧
        :param field_list: list -  来自WebSocket数据帧解析后的数据
        :return: boolean - 是否成功响应
        """
        opcode = field_list[4]
        if opcode == OPCODE.CLOSE.value:  # opcode等于0x08为收到关闭控制帧
            self.send(msg='', fin='1', rsv1='0', rsv2='0', rsv3='0', opcode='1000')  # 响应CLOSE控制帧
            self.remove_conn()  # 连接映射表中删除socket连接
            return True
        elif opcode == OPCODE.PING.value:  # opcode等于0x09为收到PING心跳包控制帧
            self.send(msg='', fin='1', rsv1='0', rsv2='0', rsv3='0', opcode='1010')  # 响应PING心跳控制帧
            return True
        elif opcode == OPCODE.PONG.value:  # opcode等于0x0A为收到PONG心跳包控制帧
            return True

    def heartbeat(self):
        """
        发送WebSocket心跳包并等待回应
        :return: Boolean - 响应心跳包返回True否则返回False
        """
        self.send(msg='', fin='1', rsv1='0', rsv2='0', rsv3='0', opcode='1001')  # 发送PING心跳包
        try:
            field_list = self.recv()
            if field_list[4] == 10:  # WebSocket控制帧为PONG心跳包
                return True
            else:  # WebSocket控制帧不为PONG心跳包
                return False
        except SocketCloseAbnormalException as exp:  # 捕获socket句柄异常关闭异常
            log_debug.logger.error(f'WebSocket {self.index}: {exp.msg}')
            return False

    def remove_conn(self):
        """
        关闭socket连接, 并从集合中删除socket句柄
        :return:
        """
        self.conn.close()  # 释放socket连接
        del self.conn_map[str(self.index)]

    def _get_socket_handle(self):
        """
        从WebSocket连接映射表中获取socket句柄，在建立连接时socket句柄可能还未创建故采用多次循环获取socket句柄
        :return: Socket句柄
        """
        for i in range(0, 10):  # 循环10次获取socket句柄
            socket = self.conn_map.get(str(self.index))
            if socket:
                return socket
            else:
                time.sleep(0.1)  # 未获取socket句柄延迟0.1s
        raise ConnMapGetSocketException()  # 抛出获取socket句柄异常

    # noinspection PyMethodMayBeStatic
    def _calc_length(self, msg):
        """
        计算数据帧中header和payload data长度
        :param msg: 接收到的数据帧字节序列长度
        :return: 数据帧总字节序列长度
        """
        payload_length = msg[1] & 127  # Payload length字段的值，十进制表示
        if payload_length == 125:
            header_length = 6  # 2+4
        elif payload_length == 126:  # 后面2个字节的extended payload length为实际长度
            payload_length = struct.unpack('>H', msg[2:4])[0]  # unpack为2个字节的unsigned short类型
            header_length = 8  # 2+2+4
        elif payload_length == 127:  # 后面8个字节的extended payload length为实际长度
            payload_length = struct.unpack('>Q', msg[2:10])[0]  # unpack为8个字节的unsigned long long类型
            header_length = 14  # 2+8+4
        else:
            payload_length = 0
            header_length = 0
        real_buffer_length = payload_length + header_length
        return real_buffer_length

    # noinspection PyMethodMayBeStatic
    def _bytify_buffer(self, buffer):
        """
        解析WebSocket数据帧中字段值
        :param buffer: bytes - 数据帧字节序列
        :return: list - 数据帧中的规定的字段值和payload data
        """
        byte_1 = hex(buffer[0])  # 数据帧第1字节, 十六进制表示
        byte_2 = hex(buffer[1])  # 数据帧第2字节, 十六进制表示
        fin = int((int(byte_1, 16) & int(0x80)) / 128)  # FIN字段值
        rsv1 = int((int(byte_1, 16) & int(0x40)) / 64)  # RSV1字段值
        rsv2 = int((int(byte_1, 16) & int(0x20)) / 32)  # RSV2字段值
        rsv3 = int((int(byte_1, 16) & int(0x10)) / 16)  # RSV3字段值
        opcode = int(byte_1, 16) & int(0x0f)  # Opcode字段值
        mask = int((int(byte_2, 16) & int(0x80)) / 128)  # 获取数据帧的MASK字段
        payload_length = int(byte_2, 16) & int(0x7f)  # 获取数据帧的payload length字段

        # 客户端数据帧MASK字段不为1
        if mask != 1:
            return None

        # 解析字段值
        if payload_length <= 125:  # 第二个字节低7位为载荷实际长度
            masking_key = buffer[2:6]
            payload_data = buffer[6:]
        elif payload_length == 126:  # 后面2个字节的Extended payload length为载荷实际长度
            payload_length = struct.unpack('>H', buffer[2:4])[0]  # unpack 2个字节的unsigned short类型
            masking_key = buffer[4:8]
            payload_data = buffer[8:]
        elif payload_length == 127:  # 后面8个字节的Extended payload length为载荷实际长度
            payload_length = struct.unpack('>Q', buffer[2:10])[0]  # unpack 8个字节的unsigned long long类型
            masking_key = buffer[10:14]
            payload_data = buffer[14:]
        else:
            return None

        # 使用Masking-key解码WebSocket数据帧
        nv_bytes = b''
        nv_str = ''
        for i, value in enumerate(payload_data):
            nv = value ^ masking_key[i % 4]  # 反掩码后的字节对应十进制数
            nv_bytes += six.int2byte(nv)
        try:
            nv_str = nv_bytes.decode('utf-8')
            return list([fin, rsv1, rsv2, rsv3, opcode, payload_length, mask, nv_str])
        except UnicodeDecodeError as exp:
            if struct.unpack('>H', nv_bytes[0:2])[0] in CLOSE_CODE._value2member_map_.keys():  # Payload_data前两个字节可能为CLOSE控制帧状态码
                nv_str = nv_bytes[2:].decode('utf-8')
                return list([fin, rsv1, rsv2, rsv3, opcode, payload_length, mask, nv_str])
            else:
                log_debug.logger.error(f'WebSocket {self.index}: {exp.reason}')
                return list([fin, rsv1, rsv2, rsv3, opcode, payload_length, mask, nv_str])
