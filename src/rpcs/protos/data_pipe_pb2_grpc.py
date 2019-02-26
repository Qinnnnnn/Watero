# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import src.rpcs.protos.data_pipe_pb2 as data__pipe__pb2


class DataFlowStub(object):
    """定义服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
          channel: A grpc.Channel.
        """
        self.TransmitData = channel.unary_unary(
            '/datapipe.DataFlow/TransmitData',
            request_serializer=data__pipe__pb2.TransmitRequest.SerializeToString,
            response_deserializer=data__pipe__pb2.TransmitReply.FromString,
        )


class DataFlowServicer(object):
    """定义服务
    """

    def TransmitData(self, request, context):
        """定义函数，输入参数为TransmitRequest，输出参数为TransmitReply
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataFlowServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'TransmitData': grpc.unary_unary_rpc_method_handler(
            servicer.TransmitData,
            request_deserializer=data__pipe__pb2.TransmitRequest.FromString,
            response_serializer=data__pipe__pb2.TransmitReply.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'datapipe.DataFlow', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
