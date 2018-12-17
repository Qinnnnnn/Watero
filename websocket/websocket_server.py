# coding: utf-8
import socket
import time
from utils.log import log_debug
from websocket.websocket_conn import WebSocket


class WebSocketServer:
    """
    基于Socket的WebSocket服务器, 循环监听端口. 接受TCP连接之后启动一个新的WebSocket Connection线程处理连接
    """

    def __init__(self):
        """
        初始化WebSocketServer类
        """
        self.index = 1  # 标识每个WebSocket连接的index
        self.socket = None  # WebSocket Server创建的Socket

    def run(self, host, port, conn_map, debug=False):
        """
        启动WebSocket服务器
        :param host: 服务器主机地址
        :param port: 服务器主机端口
        :param conn_map: WebSocket连接映射表
        :param debug: 是否为调试模式
        :return:
        """

        log_debug.logger.info('WebSocket服务器启动')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket实例

        while True:
            log_debug.logger.info('WebServer服务器开始监听 {0}:{1}'.format(host, port))
            try:
                self.socket.bind((host, port))  # Socket绑定到IP地址和端口
                self.socket.listen(5)  # 设置socket最大TCP连接挂起数
                break  # Socket绑定成功结束循环
            except OSError as exp:  # 需绑定的端口不可用
                log_debug.logger.error('WebSocket服务器启动失败: {0}'.format(exp.strerror))
                time.sleep(5)

        while True:  # 循环监听端口
            conn, address = self.socket.accept()  # 服务器响应请求, 返回WebSocket Client的socket句柄和地址
            websocket = WebSocket(conn_map=conn_map, index=self.index, conn=conn, host=address[0],
                                  remote=address, debug=debug)  # 根据连接的客户信息, 启动WebSocket连接线程
            # 线程启动
            websocket.start()
            # 写入WebSocket连接映射表
            conn_map[self.index] = conn
            self.index += 1
