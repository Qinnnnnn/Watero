#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : ws_rpc_server.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : RPC服务端
"""

import threading
import time
from concurrent import futures

import grpc

import src.websockets.utils.shared_core as shared_core
from src.rpcs.protos import data_pipe_pb2
from src.rpcs.protos import data_pipe_pb2_grpc
from utils.log import log_debug

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'  # RPC服务主机
_PORT = '6000'  # RPC服务端口


class DataFlow(data_pipe_pb2_grpc.DataFlowServicer):
    """
    RPC数据接收处理类
    """

    def TransmitData(self, request, context):
        """
        RPC数据接收处理函数
        :param request:
        :param context:
        :return:
        """
        index = request.index
        msg = request.msg
        popcorn = shared_core.PopcornModel(index, msg)
        shared_core.shared_queue.put(popcorn)
        return data_pipe_pb2.TransmitReply(status=1)


class RpcService(threading.Thread):
    """
    RPC服务类
    """

    def __init__(self):
        """
        初始化
        """
        super(RpcService, self).__init__()

    def run(self):
        """
        线程启动函数
        :return:
        """
        log_debug.logger.info('WebSocket RPC服务启动')
        self.serve()

    # noinspection PyMethodMayBeStatic
    def serve(self):
        """
        RPC服务函数
        :return:
        """
        grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        data_pipe_pb2_grpc.add_DataFlowServicer_to_server(DataFlow(), grpc_server)
        grpc_server.add_insecure_port(_HOST + ':' + _PORT)
        grpc_server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            grpc_server.stop(0)
