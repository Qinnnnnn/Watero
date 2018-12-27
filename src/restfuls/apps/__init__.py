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

from src.restfuls.apps.extension import db
from src.restfuls.apps.v1 import api_bp


def register_extension(app):
    """
    注册插件
    :param app: Flask app实例
    :return:
    """
    with app.app_context():
        db.init_app(app)
        db.create_all()


def register_blueprints(app):
    """
    注册蓝图
    :param app: Flask app实例
    :return:
    """
    app.register_blueprint(api_bp)


def create_app():
    """
    实例化Flask
    :return:
    """
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qinzerui:CleverMoon@1997@114.116.112.66:3306/watero'  # 配置MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://qinzerui:Qz.ZXJ.1997@amazon-rds-1.cq77fzszoj9b.us-east-1.rds.amazonaws.com:3306/watero'  # 配置MySQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 不追踪数据库变化
    app.config['SQLALCHEMY_ECHO'] = False  # 不打印原始SQL语句
    register_extension(app)  # 注册插件
    register_blueprints(app)  # 注册蓝图
    return app
