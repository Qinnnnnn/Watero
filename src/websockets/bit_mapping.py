#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : bit_mapping.py
Author : Zerui Qin
CreateDate : 2019-01-12 30:00:00
LastModifiedDate : 2019-01-30 10:00:00
Note : WebSocket数据帧位映射，用于映射数据帧中每位对应的含义
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
