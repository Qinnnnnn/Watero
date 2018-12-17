#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : heartbeat.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : Agent心跳包接口
"""

from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse
from flask_restful import Resource

from apps.db_model import db
from apps.db_model import AgentHeartbeatLogs
from utils import permission
from apps.v1 import api


class Heartbeat(Resource):
    """
    Agent心跳包接口
    """

    def __init__(self):
        """
        初始化
        """
        # 心跳包接口参数解析失败提示所有错误
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.parser.add_argument('access_token', required=True, type=str, help='token required')
        self.parser.add_argument('create_time', required=True, type=str, help='create_time required')

    response_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    @marshal_with(response_fields)
    def post(self):
        """
        POST方法
        :return:
        """
        # 参数验证
        args = self.parser.parse_args()
        mac_addr = args.get('mac_addr')  # mac_addr参数
        access_token = args.get('access_token')  # token参数
        create_time = args.get('create_time')  # create_time参数
        if permission.Certify.certify_agent(mac_addr, access_token):
            hb = db.session.query(AgentHeartbeatLogs).filter_by(mac_addr=mac_addr).first()
            if hb is None:
                item = AgentHeartbeatLogs(mac_addr, create_time)
                db.session.add(item)  # 新增心跳记录
                db.session.commit()
            else:
                hb.create_time = create_time
                db.session.commit()
            return {'status': '1', 'state': 'success', 'message': {'info': 'Watero server is online'}}


api.add_resource(Heartbeat, '/heartbeat', endpoint='heartbeat')
