### Watero Center服务框架

> Watero Center服务框架内部包含3个服务，分别完成节点数据通信和服务间数据通信

- HTTP服务
- WebSocket服务
- RPC服务

Watero Center对外提供HTTP服务和WebSocket服务作为数据上下行通道，而RPC服务则作为框架内部HTTP服务和WebSocket服务之间的桥梁来实现服务间通信，并保证低耦合更好地支持服务水平扩展

------

### Watero Go服务框架

> Watero Go服务框架内部包含2个服务，分别完成节点数据采集和数据投递

- 数据采集服务
- 数据投递服务

在节点上部署Watero Go作为节点的Agent服务。通过Watero Center服务框架提供的HTTP服务和WebSocket服务与Watero Center进行通信以及数据交互