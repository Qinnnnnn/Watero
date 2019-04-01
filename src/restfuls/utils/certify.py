#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : certify.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
Note : 权限验证
"""

import base64
import hmac
import time

from src.restfuls.apps.db_model import AgentRegisterLogs
from src.restfuls.apps.db_model import ClientRegisterLogs
from src.restfuls.apps.db_model import db


class Certify:
    """
    权限验证类
    """

    @staticmethod
    def certify_agent(digest, access_token):
        """
        验证Agent合法性
        :param digest: str - 消息摘要
        :param access_token: str - access_token
        :return: int - 状态码
        """
        rt = db.session.query(AgentRegisterLogs).filter_by(mac_addr=digest).first()
        if rt and rt.status == 1 and rt.access_token is not None and access_token == rt.access_token:
            if Certify.certify_token(digest, rt.access_token):  # access_token中消息摘要通过验证或未被篡改
                return 1
            else:
                return -2
        else:
            return -1

    @staticmethod
    def certify_client(client_id, client_secret):
        """
        验证Client合法性
        :param client_id: Client注册表client_id字段
        :param client_secret: Client注册表client_secret字段
        :return: int - 状态代码：1验证通过，-1验证未通过
        """
        rt = db.session.query(ClientRegisterLogs).filter_by(client_id=client_id).first()
        # TODO 采用 MD5 存储密码
        if rt and rt.status == 1 and rt.client_secret == client_secret:  # 验证通过
            return 1
        else:
            return -1

    @staticmethod
    def generate_token(msg, expire=0):
        """
        消息与当前时间戳混淆生成access_token
        :param msg: str - 用户给定的消息，需要用户保存以便之后验证token，每次产生token时的key可以是同一个key
        :param expire: int - 非负整数，默认值为0不过期，单位为秒
        :return: access_token
        """
        ts = str(int(time.time()) + expire)  # 获取当前秒级时间戳 + 时间戳阈值
        ts_byte = ts.encode("utf-8")  # 对时间戳进行UTF-8编码作为加密的key
        sha1_hex_ts_str = hmac.new(key=ts_byte, msg=msg.encode('utf-8'),
                                   digestmod='sha1').hexdigest()  # 消息摘要=SHA1(时间戳+MAC地址)
        token_str = ts + ':' + str(expire) + ':' + sha1_hex_ts_str  # access_token=时间戳 + 过期时间 + 消息摘要
        b64_token = base64.urlsafe_b64encode(token_str.encode("utf-8"))
        return b64_token.decode("utf-8")

    @staticmethod
    def certify_token(msg, access_token):
        """
        验证access_token合法性
        :param msg: 消息
        :param access_token: 访问令牌
        :return:
        """
        token_str = base64.urlsafe_b64decode(access_token.encode('utf-8')).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 3:  # 不满足access_token构造规定
            return False
        know_ts_str = token_list[0]
        know_expire = token_list[1]
        known_sha1_hex_ts_str = token_list[2]
        if int(time.time()) > int(know_ts_str) and know_expire > 0:  # access_token已过期
            return False
        else:
            calc_sha1_ts_str = hmac.new(key=know_ts_str.encode('utf-8'), msg=msg.encode('utf-8'),
                                        digestmod='sha1').hexdigest()
            return calc_sha1_ts_str == known_sha1_hex_ts_str
