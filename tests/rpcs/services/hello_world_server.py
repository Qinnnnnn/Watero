# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
File : hello_world_server.py
Author : Zerui Qin
CreateDate : 2018-12-28 10:00:00
LastModifiedDate : 2018-12-28 10:00:00
Note : gRPC server demo
"""

import time
from concurrent import futures

import grpc

from tests.rpcs.protos import hello_world_pb2
from tests.rpcs.protos import hello_world_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = 'localhost'
_PORT = '6060'


class Greeter(hello_world_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        name = request.name
        age = request.age
        return hello_world_pb2.HelloReply(message=f'Hello {name}, happy {age}th birthday!')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_world_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port(_HOST + ':' + _PORT)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
