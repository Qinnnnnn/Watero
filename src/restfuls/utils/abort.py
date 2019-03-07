#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : abort.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
LastModifiedDate : 2018-12-07 10:00:00
Note : 服务拒绝方法
"""

from flask_restful import abort


def abort_with_msg(status_code, status, state, **msg):
    """
    带消息提示的拒绝服务
    :param status_code: 错误状态码
    :param status: 响应状态码
    :param state: 响应状态类型
    :param msg: 响应错误提示信息
    :return:
    """
    response_fields = {
        'status': status,
        'state': state,
        'message': msg
    }

    abort(status_code, **response_fields)
