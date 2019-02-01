#!/usr/bin/env bash
# 切换Python虚拟环境
source activate Watero

# 将*.proto文件生成gRPC代码
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. data_pipe.proto
