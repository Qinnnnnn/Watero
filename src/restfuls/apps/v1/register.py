#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : register.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : Agent注册接口
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from src.restfuls.apps.db_model import AgentRegisterLogs
from src.restfuls.apps.db_model import db
from src.restfuls.apps.v1 import api
from utils import abort
from utils import token_core
from utils import permission


class AgentRegister(Resource):
    """
    Agent注册接口
    """

    def __init__(self):
        """
        初始化
        """
        self.is_permission = False
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('access_id', required=True, type=str, help='access_id required')
        self.get_parser.add_argument('access_secret', required=True, type=str, help='access_secret required')

        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')

    get_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.List(fields.Nested({'mac_addr': fields.String,
                                              'state': fields.String}))
    }

    post_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'access_token': fields.String}
        )
    }

    @marshal_with(get_resp_fields)
    def get(self):
        args = self.get_parser.parse_args()  # 解析参数
        access_id = args.get('access_id')
        access_secret = args.get('access_secret')
        self.is_permission = permission.Certify.certify_client(access_id, access_secret)  # 验证App是否授权
        if self.is_permission:  # App通过授权
            rt_list = db.session.execute('SELECT mac_addr,state FROM watero.agent_register_logs').fetchall()
            return {'status': '1', 'state': 'success', 'message': rt_list}

    @marshal_with(post_resp_fields)
    def post(self):
        """
        POST方法
        :return:
        """
        args = self.post_parser.parse_args()  # 解析参数
        mac_addr = args.get('mac_addr')
        access_token = token_core.generate_token(msg=mac_addr)  # 计算access_token

        rt = db.session.query(AgentRegisterLogs).filter_by(mac_addr=mac_addr).first()  # 查询Agent注册表
        if rt and rt.status == 1:
            if rt.access_token is not None:
                rt.access_token = access_token  # 旧注册记录更新access_token
                db.session.commit()
                return {'status': '2', 'state': 'success', 'message': {'access_token': access_token}}
            else:
                rt.access_token = access_token  # 新增注册记录
                db.session.commit()
                return {'status': '1', 'state': 'success', 'message': {'access_token': access_token}}
        else:
            msg = {'info': 'Access denied'}  # MAC地址不在白名单或处于非ACTIVATE状态
            abort.abort_with_msg(403, 0, 'error', **msg)


api.add_resource(AgentRegister, '/register', endpoint='register')
