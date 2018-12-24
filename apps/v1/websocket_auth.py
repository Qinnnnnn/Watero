#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : websocket_auth.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : WebSocket连接鉴权接口
"""
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from apps.v1 import api
from utils import permission
from utils import process_common


class WebSocketAuth(Resource):
    """
    WebSocket连接鉴权接口
    """

    def __init__(self):
        """
        初始化
        """
        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('access_token', required=True, type=str, help='token required')

    post_resp_fields = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    @marshal_with(post_resp_fields)
    def post(self):
        """
        POST方法
        :return:
        """
        # 参数验证
        args = self.post_parser.parse_args()
        mac_addr = args.get('mac_addr')  # mac_addr参数
        access_token = args.get('access_token')  # token参数
        if permission.Certify.certify_agent(mac_addr, access_token):  # Agent验证成功
            process_common.websocket_share_dict[mac_addr] = process_common.websocket_share_dict.pop(1)
            return {'status': '1', 'state': 'success',
                    'message': {'info': 'WebSocket connection authentication successfully'}}


api.add_resource(WebSocketAuth, '/websocketauth', endpoint='websocketauth')
