#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : mapping.py
Author : Zerui Qin
CreateDate : 2019-01-12 30:00:00
LastModifiedDate : 2019-01-30 10:00:00
Note : WebSocket数据帧字段位映射，用于映射数据帧中每字段值对应的含义
"""

from enum import Enum, unique


@unique
class OPCODE(Enum):
    """
    Opcode中4位映射值
    """
    CONTINUE = 0
    TEXT = 1
    BINARY = 2
    RESERVED_NON_CONTROL_1 = 3
    RESERVED_NON_CONTROL_2 = 4
    RESERVED_NON_CONTROL_3 = 5
    RESERVED_NON_CONTROL_4 = 6
    RESERVED_NON_CONTROL_5 = 7
    CLOSE = 8
    PING = 9
    PONG = 10
    RESERVED_CONTROL_1 = 11
    RESERVED_CONTROL_2 = 12
    RESERVED_CONTROL_3 = 13
    RESERVED_CONTROL_4 = 14
    RESERVED_CONTROL_5 = 15


@unique
class CLOSE_CODE(Enum):
    """
    CLOSE控制帧状态码映射值
    """
    CLOSE_NORMAL = 1000
    CLOSE_GOING_AWAY = 1001
    CLOSE_PROTOCOL_ERROR = 1002
    CLOSE_UNSUPPORTED = 1003
    CLOSE_NO_STATUS = 1005
    CLOSE_ABNORMAL = 1006
    Unsupported_Data = 1007
    Policy_Violation = 1008
    CLOSE_TOO_LARGE = 1009
    Missing_Extension = 1010
    Internal_Error = 1011
    Service_Restart = 1012
    Try_Again_Later = 1013
    TLS_Handshake = 1015
