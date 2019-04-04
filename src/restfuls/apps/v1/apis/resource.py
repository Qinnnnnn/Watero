#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : resource.py
Author : Zerui Qin
CreateDate : 2018-12-07 10:00:00
Note : 设备资源信息，POST
"""

from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from src.restfuls.apps.db_model import AgentResourceLogs
from src.restfuls.apps.db_model import db
from src.restfuls.utils import abort
from src.restfuls.utils.certify import Certify


class AgentResource(Resource):
    """
    设备资源信息接口
    """

    def __init__(self):
        """
        初始化
        """
        self.get_parser = reqparse.RequestParser(bundle_errors=True)  # 参数解析失败提示所有错误
        self.get_parser.add_argument('client_id', required=True, type=str, help='client_id required')
        self.get_parser.add_argument('client_secret', required=True, type=str, help='client_secret required')
        self.get_parser.add_argument('page', required=True, type=str, help='page required')

        self.post_parser = reqparse.RequestParser(bundle_errors=True)
        self.post_parser.add_argument('mac_addr', required=True, type=str, help='mac_addr required')
        self.post_parser.add_argument('access_token', required=True, type=str, help='access_token required')
        self.post_parser.add_argument('cpu_percent', required=False, type=float)
        self.post_parser.add_argument('cpu_count', required=False, type=int)
        self.post_parser.add_argument('cpu_freq_current', required=False, type=int)
        self.post_parser.add_argument('cpu_freq_min', required=False, type=int)
        self.post_parser.add_argument('cpu_freq_max', required=False, type=int)
        self.post_parser.add_argument('total_memory', required=False, type=int)
        self.post_parser.add_argument('available_memory', required=False, type=int)
        self.post_parser.add_argument('sensors_battery_percent', required=False, type=int)
        self.post_parser.add_argument('boot_time', required=False, type=str)
        self.post_parser.add_argument('create_time', required=True, type=str, help='create_time required')

        self._PAGE_SIZE = 20

    common_resp_template = {
        'status': fields.Integer,
        'state': fields.String,
        'message': fields.Nested(
            {'info': fields.String}
        )
    }

    @marshal_with(common_resp_template)
    def get(self, device_id):
        """
        POST方法
        :return:
        """
        # 参数验证
        args = self.get_parser.parse_args()
        client_id = args.get('client_id')
        client_secret = args.get('client_secret')
        page = args.get('page')

        flag = Certify.certify_client(client_id, client_secret)
        if flag == 1:
            rt = db.session.query(AgentResourceLogs).filter_by(id=device_id).limit(self._PAGE_SIZE).offset(
                (page - 1) * self._PAGE_SIZE)
            return {'status': '1', 'state': 'success', 'message': rt}
        else:
            msg = 'info: Access denied'
            abort.abort_with_msg(403, flag, 'error', msg)

    @marshal_with(common_resp_template)
    def post(self):
        """
        POST方法
        :return:
        """
        # 参数验证
        args = self.post_parser.parse_args()
        mac_addr = args.get('mac_addr')  # mac_addr参数
        access_token = args.get('access_token')  # token参数
        cpu_percent = args.get('cpu_percent')  # cpu_percent参数
        cpu_count = args.get('cpu_count')  # cpu_count参数
        cpu_freq_current = args.get('cpu_freq_current')  # cpu_freq_current参数
        cpu_freq_min = args.get('cpu_freq_min')  # cpu_freq_min参数
        cpu_freq_max = args.get('cpu_freq_max')  # cpu_freq_max参数
        total_memory = args.get('total_memory')  # total_memory参数
        sensors_battery_percent = args.get('sensors_battery_percent')  # sensors_battery_percent参数
        available_memory = args.get('available_memory')  # available_memory参数
        boot_time = args.get('boot_time')  # boot_time参数
        create_time = args.get('create_time')  # create_time参数

        flag = Certify.certify_agent(mac_addr, access_token)
        if flag == 1:
            row = AgentResourceLogs(mac_addr, cpu_percent, cpu_count, cpu_freq_current,
                                    cpu_freq_min, cpu_freq_max, total_memory, available_memory,
                                    sensors_battery_percent, boot_time, create_time)
            db.session.add(row)  # 新增设备资源信息记录
            db.session.commit()
            return {'status': '1', 'state': 'success', 'message': {'info': 'Device resource added'}}
        else:
            msg = 'info: Access denied'
            abort.abort_with_msg(403, flag, 'error', msg)
