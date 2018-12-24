#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : control.py
Author : Zerui Qin
CreateDate : 2018-12-16 10:00:00
LastModifiedDate : 2018-12-16 10:00:00
Note : Agent控制接口
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from apps.v1 import api
from utils import permission
from utils.process_common import websocket_share_dict
from websocket.websocket_common import WebSocketProtocolUtil


class Control(Resource):
    """
    Agent控制接口
    """

    def __init__(self):
        """
        初始化
        """
        # 心跳包接口参数解析失败提示所有错误
        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr field required')
        self.post_parser.add_argument('access_id', required=True, type=str, help='access_token field required')
        self.post_parser.add_argument('access_secret', required=True, type=str, help='access_token field required')
        self.post_parser.add_argument('control', required=True, type=str, help='control field required')
        self.post_parser.add_argument('create_time', required=True, type=str, help='create_time field required')

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
        args = self.post_parser.parse_args()
        access_id = args.get('access_id')  # access_id参数
        access_secret = args.get('access_secret')  # access_secret参数
        mac_addr = args.get('mac_addr')  # mac_addr参数
        control = args.get('control')
        create_time = args.get('create_time')  # create_time参数
        if permission.Certify.certify_app(access_id, access_secret):  # App通过验证
            control_msg = {
                'mac_addr': mac_addr,
                'control': control,
                'create_time': create_time
            }
            WebSocketProtocolUtil.send_frame(str(control_msg), mac_addr, websocket_share_dict)
            return {'status': '1', 'state': 'success',
                    'message': {'info': 'Control information was delivered successfully'}}


api.add_resource(Control, '/control', endpoint='control')
