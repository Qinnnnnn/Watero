#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : exception.py
Author : Zerui Qin
CreateDate : 2018-12-12 10:00:00
LastModifiedDate : 2018-12-12 10:00:00
Note : WebSocket异常类
"""


class HandshakeExceptionBase(Exception):
    """
    握手请求异常基类
    """

    def __init__(self, msg='握手请求异常'):
        self.msg = msg


class HeaderFormatException(HandshakeExceptionBase):
    """
    握手头部格式错误异常
    """

    def __init__(self):
        msg = '握手请求格式异常'
        super(HeaderFormatException, self).__init__(msg=msg)


class HeaderFieldException(HandshakeExceptionBase):
    """
    握手头部字段错误异常
    """

    def __init__(self, field, info):
        msg = "握手请求字段异常 {0}: {1}".format(field, info)
        super(HeaderFieldException, self).__init__(msg)


class HeaderFieldMultiException(HeaderFieldException):
    """
    握手头部重复异常
    """

    def __init__(self, field):
        info = '握手请求字段重复'
        super(HeaderFieldMultiException, self).__init__(field, info)


class SocketExceptionBase(Exception):
    """
    Socket异常基类
    """

    def __init__(self, msg='Socket异常'):
        self.msg = msg


class SocketCloseAbnormalException(SocketExceptionBase):
    """
    Socket异常关闭异常
    """

    def __init__(self):
        msg = 'Socket异常关闭'
        super(SocketCloseAbnormalException, self).__init__(msg=msg)
