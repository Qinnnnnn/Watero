#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : ws_rpc_server.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : 提供WebSocket信息发送RPC服务
"""

import time
from concurrent import futures

import grpc

from src.rpcs.protos import data_pipe_pb2
from src.rpcs.protos import data_pipe_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '6000'


class DataFlow(data_pipe_pb2_grpc.DataFlowServicer):

    def TransmitData(self, request, context):
        index = request.index
        msg = request.msg
        return data_pipe_pb2.TransmitReply()


def serve():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    data_pipe_pb2_grpc.add_DataFlowServicer_to_server(DataFlow(), grpc_server)
    grpc_server.add_insecure_port(_HOST + ':' + _PORT)
    grpc_server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
    serve()
