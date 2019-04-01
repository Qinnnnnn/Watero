#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : heartbeat.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
Note : Agent心跳包接口
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from src.restfuls.apps.db_model import AgentHeartbeatLogs
from src.restfuls.apps.db_model import db
from src.restfuls.utils import abort
from src.restfuls.utils.certify import Certify


class AgentHeartbeat(Resource):
    """
    Agent心跳包接口
    """

    def __init__(self):
        """
        初始化
        """
        # 心跳包接口参数解析失败提示所有错误
        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('access_token', required=True, type=str, help='token required')
        self.post_parser.add_argument('create_time', required=True, type=str, help='create_time required')

    post_response_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    @marshal_with(post_response_fields)
    def post(self):
        """
        POST方法
        :return:
        """
        # 参数验证
        args = self.post_parser.parse_args()
        mac_addr = args.get('mac_addr')
        access_token = args.get('access_token')
        create_time = args.get('create_time')

        flag = Certify.certify_agent(mac_addr, access_token)
        if flag > 0:
            rt = db.session.query(AgentHeartbeatLogs).filter_by(mac_addr=mac_addr).first()
            if rt:
                rt.create_time = create_time
                db.session.commit()
            else:
                row = AgentHeartbeatLogs(mac_addr, create_time)
                db.session.add(row)  # 新增心跳记录
                db.session.commit()
            return {'status': '1', 'state': 'success', 'message': {'info': 'Server online'}}
        else:  # Client验证未通过
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, flag, 'error', **msg)
