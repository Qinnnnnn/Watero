#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : __init__.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : 初始化Flask
"""

from flask import Flask

import src.restfuls.apps.v1.route as url_route
from src.restfuls.apps.extension import db
from src.restfuls.apps.v1 import api
from src.restfuls.apps.v1 import api_bp
from utils.get_config import get_config


def register_extension(p_app):
    """
    注册插件
    :param p_app: Flask实例
    :return:
    """
    with p_app.app_context():
        db.init_app(p_app)
        db.create_all()


def register_blueprints(p_app):
    """
    注册蓝图
    :param p_app: Flask实例
    :return:
    """
    p_app.register_blueprint(api_bp)


def register_route(p_api):
    """
    注册路由
    :param p_api: API实例
    :return:
    """
    url_route.register_url(p_api)  # 注册路由


def config_app(p_app):
    """
    配置app参数
    :param p_app: Flask实例
    :return:
    """
    config = get_config('aliyun_mysql')
    db_type = config['db_type']
    host = config['host']
    port = config['port']
    user = config['user']
    password = config['password']

    p_app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_type}+pymysql://{user}:{password}@{host}:{port}/watero'
    p_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不追踪数据库变化
    p_app.config['SQLALCHEMY_ECHO'] = False  # 不打印原始SQL语句


def create_app():
    """
    实例化Flask
    :return:
    """
    app = Flask(__name__)
    config_app(app)  # 配置app参数
    register_extension(app)  # 注册插件
    register_blueprints(app)  # 注册蓝图
    register_route(api)  # 注册路由
    return app
