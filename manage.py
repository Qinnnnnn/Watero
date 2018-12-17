#!/usr/bin/python
# -*- coding: utf-8 -*-
from multiprocessing import Process

from apps import create_app
from utils.process_common import websocket_share_dict
from websocket.websocket_server import WebSocketServer

if __name__ == '__main__':
    restful_server = create_app()  # 实例化Flask
    websocket_server = WebSocketServer()  # 实例化WebSocket Server

    flask_process = Process(target=restful_server.run, args=('0.0.0.0', 5000, False))
    websocket_process = Process(target=websocket_server.run,
                                args=('0.0.0.0', 8765, websocket_share_dict, False))

    flask_process.start()
    websocket_process.start()
    flask_process.join()
    websocket_process.join()
