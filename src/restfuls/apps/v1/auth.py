#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : auth.py
Author : Zerui Qin
CreateDate : 2018-12-16 10:00:00
LastModifiedDate : 2018-12-16 10:00:00
Note : Agent认证接口，获取access_token
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


class AgentAuth(Resource):
    """
    Agent控制接口
    """
    get_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'access_token': fields.String}
        )
    }

    def __init__(self):
        """
        初始化
        """
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr field required')

    @marshal_with(get_resp_fields)
    def get(self):
        """
        GET方法
        :return:
        """
        # 参数验证
        args = self.get_parser.parse_args()
        mac_addr = args.get('mac_addr')  # mac_addr参数
        rt = db.session.query(AgentRegisterLogs).filter(AgentRegisterLogs.mac_addr == mac_addr).first()
        if rt:
            if rt.status == 1:
                rt.access_token = token_core.generate_token(mac_addr)
                db.session.commit()
                return {'status': '1', 'state': 'success', 'message': rt}
            else:
                msg = {'info': 'Access denied'}
                abort.abort_with_msg(403, -2, 'error', **msg)
        else:
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, -1, 'error', **msg)


api.add_resource(AgentAuth, '/auth', endpoint='auth')
