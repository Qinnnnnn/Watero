#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
File : route.py
Author : Zerui Qin
CreateDate : 2019-04-01 09:50:07 
Note : 注册URL
"""
from src.restfuls.apps.v1.apis.auth import AgentAuth
from src.restfuls.apps.v1.apis.heartbeat import AgentHeartbeat
from src.restfuls.apps.v1.apis.push import AgentPush
from src.restfuls.apps.v1.apis.register import AgentRegister
from src.restfuls.apps.v1.apis.resource import AgentResource


def register_url(api):
    """
    注册URL
    :param api:
    :return:
    """
    api.add_resource(AgentRegister, '/register', endpoint='register')
    api.add_resource(AgentAuth, '/auth', endpoint='auth')
    api.add_resource(AgentPush, '/push', endpoint='push')
    api.add_resource(AgentHeartbeat, '/heartbeat/', endpoint='heartbeat')
    api.add_resource(AgentResource, '/resource', endpoint='resource')
