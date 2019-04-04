#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : abort.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
Note : 服务拒绝方法
"""

from flask_restful import abort


def abort_with_msg(http_status_code, status, state, msg=''):
    """
    带消息提示的拒绝服务方法
    :param http_status_code: int - HTTP请求错误状态码
    :param status: int - 响应状态码
    :param state: str - 响应状态类型
    :param msg: str - 响应错误提示信息
    :return:
    """
    if msg != '':
        response = {
            'status': status,
            'state': state,
            'message': msg
        }
        abort(http_status_code, **response)
    else:
        abort(http_status_code)
