#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : token_core.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
LastModifiedDate : 2018-12-07 10:00:00
Note : 生成access_token, 验证access_token
"""

import time
import base64
import hmac


def generate_token(msg, expire=31536000):
    """
    消息与当前时间戳混淆生成token
    :param msg: str - 用户给定的消息,需要用户保存以便之后验证token,每次产生token时的key可以是同一个key
    :param expire: int - 默认值为365天过期
    :return: token
    """
    # 获取当前秒级时间戳 + 时间戳阈值
    ts_str = str(int(time.time()) + expire)
    # 对时间戳进行UTF-8编码作为加密的key
    ts_byte = ts_str.encode("utf-8")
    # 消息摘要=SHA1(时间戳+MAC地址)
    sha1_hex_ts_str = hmac.new(key=ts_byte, msg=msg.encode('utf-8'), digestmod='sha1').hexdigest()
    # Token=时间戳+消息摘要
    token_str = ts_str + ':' + sha1_hex_ts_str
    b64_token = base64.urlsafe_b64encode(token_str.encode("utf-8"))
    return b64_token.decode("utf-8")


def certify_token(mag, token):
    """
    验证token合法性
    :param mag: 消息体
    :param token: 待验证token
    :return:
    """
    token_str = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:  # 不满足规定token构造
        return False
    know_ts_str = token_list[0]
    if int(know_ts_str) < int(time.time()):  # token已超过阈值
        return False
    known_sha1_ts_str = token_list[1]
    calc_sha1_ts_str = hmac.new(key=know_ts_str.encode('utf-8'), msg=mag.encode('utf-8'),
                                digestmod='sha1').hexdigest()
    if calc_sha1_ts_str != known_sha1_ts_str:  # 验证token
        return False  # Token验证失败
    return True  # Token验证成功
