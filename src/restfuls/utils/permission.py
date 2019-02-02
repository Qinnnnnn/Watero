#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : permission.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
LastModifiedDate : 2018-12-07 10:00:00
Note : 验证Agent合法性
"""

from src.restfuls.apps.db_model import AgentRegisterLogs
from src.restfuls.apps.db_model import ClientRegisterLogs
from src.restfuls.apps.db_model import db
from src.restfuls.utils import token_core


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
        :return: tuple - (Agent是否合法, 状态代码)
        """
        rt = db.session.query(AgentRegisterLogs).filter_by(mac_addr=mac_addr).first()
        if rt:  # MAC地址在白名单内
            if rt.status == 1:  # Agent处于可用状态
                if rt.access_token is None:  # Agent未注册
                    return False, -3
                elif access_token != rt.access_token:  # Agent的access_token错误
                    return False, -4
                elif token_core.certify_token(mac_addr, rt.access_token) is False:  # Agent的access_token过期
                    return False, -5
                else:
                    return True, 1
            else:  # Agent处于不可用状态
                return False, -2
        else:  # MAC地址不在白名单内
            return False, -1

    @staticmethod
    def certify_client(client_id, client_secret):
        """
        Client验证方法
        :param client_id: Client注册表client_id字段
        :param client_secret: Client注册表client_secret字段
        :return: tuple - (Agent是否合法, 状态代码)
        """
        rt = db.session.query(ClientRegisterLogs).filter_by(client_id=client_id).first()
        # TODO 采用 MD5 存储密码
        if rt:  # 存在client_id记录
            if rt.status == 1:  # client_id状态为可用
                if rt.client_secret == client_secret:  # client_id对应的client_secret正确
                    return True, 1
                else:  # client_id对应的client_secret错误
                    return False, -3
            else:  # client_id状态为不可用
                return False, -2
        else:  # 不存在client_id记录
            return False, -1
