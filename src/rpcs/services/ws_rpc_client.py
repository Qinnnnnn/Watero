#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : ws_rpc_client.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : RPC客户端
"""

import grpc

from src.rpcs.protos import data_pipe_pb2
from src.rpcs.protos import data_pipe_pb2_grpc

_HOST = 'localhost'  # RPC服务主机
_PORT = '6000'  # RPC服务端口


def run(index, msg):
    """
    RPC服务端调用
    :param index: str - Socket索引
    :param msg: str - 待发送信息
    :return:
    """
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    grpc_client = data_pipe_pb2_grpc.DataFlowStub(channel=conn)
    response = grpc_client.TransmitData(
        data_pipe_pb2.TransmitRequest(index=index, msg=msg))
    print(response.status)


if __name__ == '__main__':
    run(index='1', msg='Hello agent')
