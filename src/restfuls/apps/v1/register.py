#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : register.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : Agent注册表接口，对agent_register_logs表CRUD操作
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from src.restfuls.apps.db_model import AgentRegisterLogs
from src.restfuls.apps.db_model import db
from src.restfuls.apps.v1 import api
from src.restfuls.utils import abort
from src.restfuls.utils.permission import Certify


class AgentRegister(Resource):
    """
    Agent注册表接口
    """

    get_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.List(fields.Nested({'mac_addr': fields.String,
                                              'status': fields.Integer}))
    }

    common_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    PAGE_SIZE = 20  # 每页数据数量

    def __init__(self):
        """
        初始化
        """
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.get_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.get_parser.add_argument('page', required=True, type=int, help='page required')

        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.post_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('status', required=True, type=int, help='status required')

        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.put_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.put_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.put_parser.add_argument('status', required=True, type=int, help='status required')

        self.del_parser = reqparse.RequestParser()
        self.del_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.del_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.del_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')

    @marshal_with(get_resp_fields)
    def get(self):
        args = self.get_parser.parse_args()  # 解析参数
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        PAGE_INDEX = args.get('page')  # 页数索引

        flag_status = Certify.certify_client(client_id, client_secret)  # Client验证
        if flag_status[0]:  # Client验证通过，获取Agent注册记录
            rt = db.session.query(AgentRegisterLogs).limit(self.PAGE_SIZE).offset((PAGE_INDEX - 1) * self.PAGE_SIZE)
            return {'status': '1', 'state': 'success', 'message': rt}
        else:
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, flag_status[1], 'error', **msg)

    @marshal_with(common_resp_fields)
    def post(self):
        """
        POST方法
        :return:
        """
        args = self.post_parser.parse_args()  # 解析参数
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        mac_addr = args.get('mac_addr')
        status = args.get('status')

        flag_status = Certify.certify_client(client_id, client_secret)  # Client验证
        if flag_status[0]:  # Client验证通过，添加Agent注册记录
            rt = db.session.query(AgentRegisterLogs).filter(AgentRegisterLogs.mac_addr == mac_addr).first()
            if rt:
                msg = {'info': 'Add denied'}
                abort.abort_with_msg(403, -4, 'error', **msg)
            else:
                record = AgentRegisterLogs(mac_addr, None, status)
                db.session.add(record)
                db.session.commit()
                return {'status': '1', 'state': 'success', 'message': {'info': 'Agent added'}}
        else:
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, flag_status[1], 'error', **msg)

    @marshal_with(common_resp_fields)
    def put(self):
        """
        PUT方法
        :return:
        """
        args = self.put_parser.parse_args()  # 解析参数
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        mac_addr = args.get('mac_addr')
        status = args.get('status')

        flag_status = Certify.certify_client(client_id, client_secret)  # Client验证
        if flag_status[0]:  # Client验证通过，修改Agent注册记录
            rt = db.session.query(AgentRegisterLogs).filter(AgentRegisterLogs.mac_addr == mac_addr).first()
            if rt:
                rt.status = status
                db.session.commit()
                return {'status': '1', 'state': 'success', 'message': {'info': 'Agent updated'}}
            else:
                msg = {'info': 'Update denied'}
                abort.abort_with_msg(403, -5, 'error', **msg)
        else:
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, flag_status[1], 'error', **msg)

    @marshal_with(common_resp_fields)
    def delete(self):
        """
        DELETE方法
        :return:
        """
        args = self.del_parser.parse_args()  # 解析参数
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        mac_addr = args.get('mac_addr')

        flag_status = Certify.certify_client(client_id, client_secret)  # Client验证
        if flag_status[0]:  # Client验证通过，删除Agent注册记录
            rt = db.session.query(AgentRegisterLogs).filter(AgentRegisterLogs.mac_addr == mac_addr).first()
            if rt:
                db.session.delete(rt)
                db.session.commit()
                return {'status': '1', 'state': 'success', 'message': {'info': 'Agent deleted'}}
            else:
                msg = {'info': 'Delete denied'}
                abort.abort_with_msg(403, -6, 'error', **msg)
        else:
            msg = {'info': 'Access denied'}
            abort.abort_with_msg(403, flag_status[1], 'error', **msg)


api.add_resource(AgentRegister, '/register', endpoint='register')
