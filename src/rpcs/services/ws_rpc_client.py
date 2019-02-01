#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : ws_rpc_server.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : 调用WebSocket发送信息RPC服务
"""

import grpc

from src.rpcs.protos import data_pipe_pb2
from src.rpcs.protos import data_pipe_pb2_grpc

_HOST = 'localhost'
_PORT = '6000'


def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    grpc_client = data_pipe_pb2_grpc.DataFlowStub(channel=conn)
    response = grpc_client.TransmitData(
        data_pipe_pb2.TransmitRequest(index='2', msg='Hello agent'))
    print(response.status)


if __name__ == '__main__':
    run()
