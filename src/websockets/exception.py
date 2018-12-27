#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : exception.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket异常类
"""


class InvalidHandshake(Exception):
    """
    握手请求异常基类
    """

    def __init__(self, message):
        self.message = message


class InvalidFormat(InvalidHandshake):
    """
    HTTP格式错误时引发异常
    """

    def __init__(self, message):
        super(InvalidFormat, self).__init__(message)


class InvalidHeader(InvalidHandshake):
    """
    HTTP头部缺失或无效时引发异常
    """

    def __init__(self, field, info):
        message = "Invalid header {0}: {1}".format(field, info)
        super(InvalidHeader, self).__init__(message)


class InvalidMultiHeader(InvalidHeader):
    """
    HTTP头部重复时引发异常
    """

    def __init__(self, field, info='header repeat'):
        super(InvalidMultiHeader, self).__init__(field, info)
