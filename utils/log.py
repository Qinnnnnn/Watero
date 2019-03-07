#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : log.py
Author : Zerui Qin
CreateDate : 2018-12-06 10:00:00
LastModifiedDate : 2018-12-06 10:00:00
Note : 输出日志
"""
import logging
import logging.handlers
import os


class Log:
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename, level='INFO', interval=1, when='D', backCount=3,
                 fmt='[%(asctime)s] [%(levelname)s] file:%(filename)s - line:%(lineno)s - %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        """
        初始化
        :param filename: 日志文件路径
        :param level: 日志等级
        :param interval: 切分日志时间长度
        :param when: 切分日志时间单位
        :param backCount: 日志备份数量
        :param fmt: 日志格式
        """
        format_str = logging.Formatter(fmt=fmt, datefmt=datefmt)  # 获取Formatter对象, 设置日志输出格式
        sh = logging.StreamHandler()  # 控制台输出处理器
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = logging.handlers.TimedRotatingFileHandler(filename=filename, interval=interval, when=when,
                                                       backupCount=backCount,
                                                       encoding='utf-8')  # 文件输出处理器, 文件按时切分
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger = logging.Logger(filename)  # 获取Logger对象
        self.logger.setLevel(self.level_map.get(level))  # 设置日志级别
        self.logger.addHandler(sh)  # 把控制台输出对象加到logger里
        self.logger.addHandler(th)  # 把文件输出对象加到logger里


path = os.getcwd()
log_debug = Log(path + '/logs/debug.log', 'DEBUG')
log_info = Log(path + '/logs/info.log', 'INFO')
log_warning = Log(path + '/logs/warning.log', 'WARNING')
log_error = Log(path + '/logs/error.log', 'ERROR')
log_critical = Log(path + '/logs/critical.log', 'CRITICAL')
