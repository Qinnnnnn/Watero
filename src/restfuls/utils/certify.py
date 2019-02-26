#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : certify.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
LastModifiedDate : 2018-12-07 10:00:00
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
    def certify_agent(mac_addr, access_token):
        """
        通过MAC地址和access_token来判断Agent是否合法
        :param mac_addr: str - Agent的MAC地址
        :param access_token: str - Agent的access_token
        :return: int - 状态代码
        """
        rt = db.session.query(AgentRegisterLogs).filter_by(mac_addr=mac_addr).first()
        if rt:  # MAC地址在白名单内
            if rt.status == 1:  # Agent处于可用状态
                if rt.access_token is None:  # Agent未注册
                    return -3
                elif access_token != rt.access_token:  # Agent的access_token错误
                    return -4
                elif Certify.certify_token(mac_addr, rt.access_token) is False:  # Agent的access_token过期
                    return -5
                else:
                    return 1
            else:  # Agent处于不可用状态
                return -2
        else:  # MAC地址不在白名单内
            return -1

    @staticmethod
    def certify_client(client_id, client_secret):
        """
        Client验证方法
        :param client_id: Client注册表client_id字段
        :param client_secret: Client注册表client_secret字段
        :return: int - 状态代码
        """
        rt = db.session.query(ClientRegisterLogs).filter_by(client_id=client_id).first()
        # TODO 采用 MD5 存储密码
        if rt:  # 存在client_id记录
            if rt.status == 1:  # client_id状态为可用
                if rt.client_secret == client_secret:  # client_id对应的client_secret正确
                    return 1
                else:  # client_id对应的client_secret错误
                    return -3
            else:  # client_id状态为不可用
                return -2
        else:  # 不存在client_id记录
            return -1

    @staticmethod
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

    @staticmethod
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
