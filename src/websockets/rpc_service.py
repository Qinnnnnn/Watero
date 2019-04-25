#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : rpc_server.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : RPC Server
"""

import threading
import time
from concurrent import futures

import grpc

import utils.msg_queue as msg_queue
from src.rpcs.protos import data_pipe_pb2
from src.rpcs.protos import data_pipe_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'  # RPC服务主机
_PORT = '6000'  # RPC服务端口


class DataFlow(data_pipe_pb2_grpc.DataFlowServicer):
    """
    RPC数据接收处理类
    """

    def TransmitData(self, request, context):
        """
        RPC服务处理函数，接收到RPC数据写入共享队列
        :param request:
        :param context:
        :return:
        """
        index = request.index
        msg = request.msg
        popcorn = msg_queue.PopcornModel(index, msg)
        msg_queue.mq.put(popcorn)
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
