#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : __init__.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : 初始化V1.0 API蓝图
"""

from flask import Blueprint
from flask_restful import Api

url_prefix = '/api/v1'
api_bp = Blueprint('api', __name__, url_prefix=url_prefix)
api = Api(api_bp)

from apps.v1.register import Register
from apps.v1.heartbeat import Heartbeat
from apps.v1.device_resource import DeviceResource
from apps.v1.control import Control
