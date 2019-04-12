#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : websocket_manage.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : 拉起WebSocket服务入口
"""

from src.websockets.server import WebSocketServer

if __name__ == '__main__':
    _HOST = '0.0.0.0'
    _PORT = 5001
    ws_server = WebSocketServer()  # 实例化WebSocket服务
    ws_server.run(host=_HOST, port=_PORT, debug=False)
