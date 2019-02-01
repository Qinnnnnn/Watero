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

from src.websockets.core.exception import SocketCloseAbnormalException, ConnMapGetSocketException
from src.websockets.core.frame_field import OPCODE
from utils.log import log_debug


class Transmission:
    """
    WebSocket协议数据传输类
    """

    def __init__(self, index, conn_map):
        """
        初始化
        :param index: int/str - Socket索引号
        :param conn_map: dict - WebSocket连接映射表
        """
        self.index = index
        self.conn_map = conn_map
        self.conn = self._get_socket_handle()

    def send_frame(self, msg, frame_frrro=b'\x81'):
        """
        WebSocket数据帧发送函数
        :param msg: str - 待发送消息
        :param frame_frrro: byte - 数据帧的第1个字节，FIN RSV1 RSV2 RSV3 opcode字段
        :return:
        """
        msg_length = len(msg.encode())  # 计算消息字节序列长度
        if msg_length <= 125:  # 当消息内容长度小于等于125时, 数据帧的第2个字节低7位直接标示消息内容的长度
            frame_frrro += struct.pack('B', msg_length)
        elif msg_length <= 65535:  # 当消息内容长度需要2个字节来表示时, 此字节低7位取值为126, 由后2个字节标示信息内容的长度
            frame_frrro += struct.pack('B', 126)
            frame_frrro += struct.pack('>H', msg_length)  # 以big endian包装为short类型(2 bytes)的结构体
        elif msg_length <= (2 ^ 64 - 1):  # 当消息内容长度需要8个字节来表示时,此字节低7位取值为127, 由后8个字节标示信息内容的长度
            frame_frrro += struct.pack('B', 127)
            frame_frrro += struct.pack('>Q', msg_length)  # 以big endian包装为long long类型(8 bytes)结构体
        else:
            # TODO 支持消息分片发送
            log_debug.logger.error('消息过长')
        message = frame_frrro + msg.encode('utf-8')
        self.conn.send(message)

    def recv_frame(self):
        """
        WebSocket数据帧接收函数
        :return: bytes - 接收到的数据帧
        """
        recv_buffer = b''
        while True:
            recv_buffer += self.conn.recv(1024)
            if len(recv_buffer) == 0:  # Socket异常关闭，未接收数据
                raise SocketCloseAbnormalException()  # 抛出Socket异常关闭的异常
            else:  # Socket正常接收数据
                rt_list = self._bytify_buffer(buffer=recv_buffer)  # 解析数据帧字节序列
                if rt_list[0] == 0:  # FIN字段为0
                    # TODO 接收WebSocket分片的数据帧
                    pass
                elif rt_list[0] == 1:  # FIN字段为1
                    total_byte_length = self._calc_frame_length(recv_buffer)
                    recv_buffer_length = len(recv_buffer)
                    if recv_buffer_length < total_byte_length:  # WebSocket Server数据帧未接收完整
                        continue
                    else:  # WebSocket Server数据帧接收完整
                        rt_list.append(recv_buffer)
                        return rt_list

    def respond_control_frame(self, frame_tuple):
        """
        响应WebSocket Client控制帧
        :param frame_tuple: tuple -  来自WebSocket Client数据帧解析后的数据
        :return: boolean - 是否成功响应
        """
        opcode = frame_tuple[4]
        if opcode == OPCODE.CLOSE.value:  # opcode等于0x08为收到关闭控制帧
            self.send_frame(msg='', frame_frrro=b'\x88')  # 响应CLOSE控制帧
            self.remove_conn()  # 连接映射表中删除socket连接
            return True
        elif opcode == OPCODE.PING.value:  # opcode等于0x09为收到PING心跳包控制帧
            self.send_frame(msg='', frame_frrro=b'\x8A')  # 响应PING心跳控制帧
            return True
        elif opcode == OPCODE.PONG.value:  # opcode等于0x0A为收到PONG心跳包控制帧
            return True
        else:  # opcode为其他情况为成功响应
            return False

    def send_heartbeat(self):
        """
        发送WebSocket心跳包并等待回应
        :return: Boolean - 响应心跳包返回True否则返回False
        """
        self.send_frame(msg='', frame_frrro=b'\x89')  # 发送PING心跳包
        try:
            rt_list = self.recv_frame()  # 接收WebSocket 数据帧
            if rt_list[4] == 10:  # WebSocket控制帧为PONG心跳包
                return True
            else:  # WebSocket控制帧不为PONG心跳包
                return False
        except SocketCloseAbnormalException as exp:  # 捕获socket句柄异常关闭异常
            log_debug.logger.error('WebSocket {0} {1}'.format(self.index, exp.msg))
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
        从WebSocket连接映射表中获取socket句柄，在建立连接时socket句柄可能还未创建故采用死循环直至获取socket句柄
        :return: Socket句柄
        """
        socket_handle = None
        for i in range(0, 10):  # 循环10次获取socket句柄
            socket_handle = self.conn_map.get(str(self.index))
            if socket_handle:
                break  # 提前获取socket句柄结束循环
            else:
                time.sleep(0.1)  # 未获取socket句柄延迟0.1s
        if socket_handle:
            return socket_handle
        else:
            raise ConnMapGetSocketException()  # 连接映射表获取socket句柄异常

    # noinspection PyMethodMayBeStatic
    def _calc_frame_length(self, msg):
        """
        计算WebSocket Client发送的数据帧中header和payload data的实际长度
        :param msg: WebSocket Server接收到的数据
        :return: 数据帧字节应有序列长度
        """
        frame_payload_length = msg[1] & 127  # 获取第2个字节中payload length字段的值
        if frame_payload_length == 126:  # 后面2个字节的extended payload length为实际长度
            frame_payload_length = struct.unpack('>H', msg[2:4])[0]  # unpack为2个字节的unsigned short类型
            frame_header_length = 8  # 2+2+4
        elif frame_payload_length == 127:  # 后面8个字节的extended payload length为实际长度
            frame_payload_length = struct.unpack('>Q', msg[2:10])[0]  # unpack为8个字节的unsigned long long类型
            frame_header_length = 14  # 2+8+4
        else:
            frame_header_length = 6  # 2+4
        total_byte_length = frame_payload_length + frame_header_length
        return total_byte_length

    # noinspection PyMethodMayBeStatic
    def _bytify_buffer(self, buffer):
        """
        解析WebSocket数据帧中字段值
        :param buffer: bytes - 数据帧字节序列
        :return: tuple - Payload data和数据帧中的规定的字段值
        """
        frame_byte_1 = hex(buffer[0])  # 数据帧第1字节, 十六进制表示
        frame_byte_2 = hex(buffer[1])  # 数据帧第2字节, 十六进制表示
        frame_fin = int((int(frame_byte_1, 16) & int(0x80)) / 128)  # FIN字段值
        frame_rsv1 = int((int(frame_byte_1, 16) & int(0x40)) / 64)  # RSV1字段值
        frame_rsv2 = int((int(frame_byte_1, 16) & int(0x20)) / 32)  # RSV2字段值
        frame_rsv3 = int((int(frame_byte_1, 16) & int(0x10)) / 16)  # RSV3字段值
        frame_opcode = int(frame_byte_1, 16) & int(0x0f)  # opcode字段值
        frame_mask = int((int(frame_byte_2, 16) & int(0x80)) / 128)  # 获取数据帧的MASK字段
        frame_payload_length = int(frame_byte_2, 16) & int(0x7f)  # 获取数据帧的Payload length字段

        # WebSocket Client发送的消息中MASK字段不为1
        if frame_mask != 1:
            return list([frame_fin, frame_rsv1, frame_rsv2, frame_rsv3, frame_opcode, frame_mask,
                         frame_payload_length, None])

        if frame_payload_length == 126:  # 后面2个字节的Extended payload length为实际长度
            frame_payload_length = struct.unpack('>H', buffer[2:4])[0]  # unpack 2个字节的unsigned short类型
            frame_masking_key = buffer[4:8]
            frame_payload_data = buffer[8:]
        elif frame_payload_length == 127:  # 后面8个字节的Extended payload length为实际长度
            frame_payload_length = struct.unpack('>Q', buffer[2:10])[0]  # unpack 8个字节的unsigned long long类型
            frame_masking_key = buffer[10:14]
            frame_payload_data = buffer[14:]
        else:
            frame_masking_key = buffer[2:6]
            frame_payload_data = buffer[6:]

        # 使用Masking-key解码WebSocket Client发来的消息
        nv_bytes = b''
        for i, value in enumerate(frame_payload_data):
            nv = value ^ frame_masking_key[i % 4]  # 反掩码后的字节对应十进制数
            nv_bytes += six.int2byte(nv)
        try:
            res = nv_bytes.decode('utf-8')
            return list(
                [frame_fin, frame_rsv1, frame_rsv2, frame_rsv3, frame_opcode, frame_mask, frame_payload_length, res])
        except UnicodeDecodeError as exp:
            log_debug.logger.error('WebSocket {0}: {1}'.format(self.index, exp.reason))
            return list([frame_fin, frame_rsv1, frame_rsv2, frame_rsv3, frame_opcode, frame_mask,
                         frame_payload_length, None])
