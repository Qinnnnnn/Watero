#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : db_model.py
Author : Zerui Qin
CreateDate : 2018-11-18 10:00:00
LastModifiedDate : 2018-11-18 10:00:00
Note : 定义SQLAlchemy数据模型
"""

from src.restfuls.apps.extension import db


class ClientRegisterLogs(db.Model):
    """
    Client注册表
    """
    __tablename__ = 'client_register_logs'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    client_id = db.Column(db.Text, nullable=True)
    client_secret = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, access_id, access_secret, status):
        self.client_id = access_id
        self.client_secret = access_secret
        self.status = status

    def __repr__(self):
        return '<ClientRegisterLogs>'


class AgentRegisterLogs(db.Model):
    """
    Agent注册表
    """
    __tablename__ = 'agent_register_logs'
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    mac_addr = db.Column(db.String(17), nullable=False, unique=True)
    access_token = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, mac_addr, access_token, status):
        self.mac_addr = mac_addr
        self.access_token = access_token
        self.status = status

    def __repr__(self):
        return '<AgentRegisterLogs>'


class AgentHeartbeatLogs(db.Model):
    """
    Agent心跳包数据表
    """
    __tablename__ = 'agent_heartbeat_logs'
    id = db.Column(db.INT, nullable=False, autoincrement=True, primary_key=True)
    mac_addr = db.Column(db.String(17), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, mac_addr, create_time):
        self.mac_addr = mac_addr
        self.create_time = create_time

    def __repr__(self):
        return '<AgentHeartbeatLogs>'


class AgentResourceLogs(db.Model):
    """
    设备资源信息数据表
    """
    __tablename__ = 'agent_resource_logs'
    id = db.Column(db.INT, nullable=False, autoincrement=True, primary_key=True)
    mac_addr = db.Column(db.String(17), nullable=False)
    cpu_percent = db.Column(db.Float)
    cpu_count = db.Column(db.Integer)
    cpu_freq_current = db.Column(db.Integer)
    cpu_freq_min = db.Column(db.Integer)
    cpu_freq_max = db.Column(db.Integer)
    total_memory = db.Column(db.Integer)
    available_memory = db.Column(db.Integer)
    sensors_battery_percent = db.Column(db.Integer)
    boot_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, mac_addr, cpu_percent, cpu_count, cpu_freq_current, cpu_freq_min, cpu_freq_max,
                 total_memory, available_memory, sensors_battery_percent, boot_time, create_time):
        self.mac_addr = mac_addr  # MAC地址
        self.cpu_percent = cpu_percent  # CPU占用率
        self.cpu_count = cpu_count  # CPU非逻辑核心数
        self.cpu_freq_current = cpu_freq_current  # CPU当前频率
        self.cpu_freq_min = cpu_freq_min  # CPU最小频率
        self.cpu_freq_max = cpu_freq_max  # CPU最大频率
        self.total_memory = total_memory  # 总内存
        self.available_memory = available_memory  # 可用内存
        self.sensors_battery_percent = sensors_battery_percent  # 电量百分比
        self.boot_time = boot_time  # 启动时间
        self.create_time = create_time  # 记录产生时间

    def __repr__(self):
        return '<AgentResourceLogs>'
