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
from utils import abort
from utils import token_core


class Certify:
    """
    验证Agent信息
    """

    @staticmethod
    def certify_agent(mac_addr, access_token):
        """
        通过MAC地址和access_token来判断Agent是否合法
        :param mac_addr:
        :param access_token:
        :return: boolean - Agent是否合法
        """
        rt = db.session.query(AgentRegisterLogs).filter_by(mac_addr=mac_addr).first()
        if rt and rt.status == 1:
            if rt.access_token is None:  # 未注册
                msg = {'info': 'Access token is null, please register first'}
                abort.abort_with_msg(403, 2, 'error', **msg)
                return False
            elif access_token != rt.access_token:  # access_token错误
                msg = {'info': 'Access denied'}
                abort.abort_with_msg(403, 0, 'error', **msg)
                return False
            elif token_core.certify_token(mac_addr, rt.access_token) is False:  # token已过期
                msg = {'info': 'Access token is expired, please register again'}
                abort.abort_with_msg(403, 3, 'error', **msg)
                return False
            else:
                return True
        else:
            msg = {'info': 'Access denied'}  # MAC地址不在白名单或处于非ACTIVATE状态
            abort.abort_with_msg(403, 0, 'error', **msg)
            return False

    @staticmethod
    def abort_agent(flag_status):
        """
        拒绝Agent访问方法
        :param flag_status:
        :return:
        """
        if flag_status==1:


    @staticmethod
    def certify_client(access_id, access_secret):
        rt = db.session.query(ClientRegisterLogs).filter_by(access_id=access_id).first()
        # TODO 采用 MD5 存储密码
        if rt:  # 存在access_id记录
            if rt.status == 1:  # access_id状态为可用
                if rt.access_secret == access_secret:  # access_id对应的access_secret正确
                    return 0
                else:  # access_id对应的access_secret错误
                    return 3
            else:  # access_id状态为不可用
                return 2
        else:  # 不存在access_id记录
            return 1

    @staticmethod
    def abort_client(flag_status):
        """
        拒绝Client访问方法
        :param flag_status: 错误状态码
        :return:
        """
        if flag_status == 1:
            msg = {'info': 'Access denied, access_id does not exist'}
            abort.abort_with_msg(403, 1, 'error', **msg)
        elif flag_status == 2:
            msg = {'info': 'Access denied, access_id is deactivate'}
            abort.abort_with_msg(403, 2, 'error', **msg)
        elif flag_status == 3:
            msg = {'info': 'Access denied, access_secret is incorrect'}
            abort.abort_with_msg(403, 3, 'error', **msg)
