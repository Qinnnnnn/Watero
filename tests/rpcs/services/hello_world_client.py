# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : hello_world_client.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : gRPC client demo
"""

import grpc

from tests.rpcs.protos import hello_world_pb2
from tests.rpcs.protos import hello_world_pb2_grpc

_HOST = 'localhost'
_PORT = '6060'


def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = hello_world_pb2_grpc.GreeterStub(channel=conn)
    response = client.SayHello(hello_world_pb2.HelloRequest(name='Clever Moon', age=18))
    print("received: " + response.message)


if __name__ == '__main__':
    run()
