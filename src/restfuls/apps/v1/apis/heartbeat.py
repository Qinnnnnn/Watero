#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : heartbeat.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
Note : Agent心跳包接口，GET/POST
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
        self.get_parser = reqparse.RequestParser(bundle_errors=True)  # 心跳包接口参数解析失败提示所有错误
        self.get_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.get_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.get_parser.add_argument('page', required=True, type=int, help='page required')
        self.get_parser.add_argument('mac_addr', required=False, type=str)

        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('access_token', required=True, type=str, help='token required')
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('create_time', required=True, type=str, help='create_time required')

        self._PAGE_SIZE = 20  # 每页数据数量

    get_resp_template = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'mac_addr': fields.String(default=''),
             'last_connection_time': fields.String(attribute='create_time', default='')}
        )
    }

    post_resp_template = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.String
    }

    @marshal_with(get_resp_template)
    def get(self):
        """
        GET方法
        :return:
        """
        args = self.get_parser.parse_args()
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        page = args.get('page')
        mac_addr = args.get('mac_addr')

        flag = Certify.certify_client(client_id, client_secret)
        if flag == 1:
            if mac_addr:
                rt = db.session.query(AgentHeartbeatLogs).filter_by(mac_addr=mac_addr).all()
            else:
                rt = db.session.query(AgentHeartbeatLogs).limit(self._PAGE_SIZE).offset(
                    (page - 1) * self._PAGE_SIZE).all()
            return {'status': '1', 'state': 'success', 'message': rt}
        else:
            msg = 'Access denied'
            abort.abort_with_msg(403, flag, 'error', msg)

    @marshal_with(post_resp_template)
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
        if flag == 1:
            rt = db.session.query(AgentHeartbeatLogs).filter_by(mac_addr=mac_addr).first()
            if rt:
                rt.create_time = create_time  # 修改最后心跳时间
                db.session.commit()
            else:
                row = AgentHeartbeatLogs(mac_addr, create_time)
                db.session.add(row)  # 新增心跳记录
                db.session.commit()
            return {'status': '1', 'state': 'success', 'message': 'Server online'}
        else:
            msg = 'Access denied'
            abort.abort_with_msg(403, flag, 'error', msg)
