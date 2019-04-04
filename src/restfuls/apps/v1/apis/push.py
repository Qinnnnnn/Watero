#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : push.py
Author : Zerui Qin
CreateDate : 2018-12-16 10:00:00
LastModifiedDate : 2018-12-16 10:00:00
Note : Agent控制接口，POST
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

import src.rpcs.services.ws_rpc_client as ws_rpc_client
from src.restfuls.utils import abort
from src.restfuls.utils.certify import Certify


class AgentPush(Resource):
    """
    Agent信息推送接口
    """

    def __init__(self):
        """
        初始化
        """
        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.post_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('message', required=True, type=str, help='message required')
        self.post_parser.add_argument('create_time', required=True, type=str, help='create_time required')

    post_resp_template = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    @marshal_with(post_resp_template)
    def post(self):
        """
        POST方法
        :return:
        """
        args = self.post_parser.parse_args()
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        mac_addr = args.get('mac_addr')
        message = args.get('message')
        create_time = args.get('create_time')

        flag = Certify.certify_client(client_id, client_secret)
        if flag == 1:  # Client验证通过
            control_msg = {
                'mac_addr': mac_addr,
                'message': message,
                'create_time': create_time
            }
            status = ws_rpc_client.run(index=mac_addr, msg=str(control_msg))
            if status:
                return {'status': '1', 'state': 'success',
                        'message': {'info': 'Message pushed successfully'}}
            else:
                return {'status': '-1', 'state': 'error',
                        'message': {'info': 'Message pushed failed'}}
        else:  # Client验证未通过
            msg = 'info: Access denied'
            abort.abort_with_msg(403, flag, 'error', msg)
