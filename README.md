# Watero Center

## 介绍

* Watero Center是一项数据接收投递转发服务
* [Watero Go](https://github.com/Qinnnnnn/Watero_Go) 是Watero Center项目部署于节点的Agent服务, 用于采集节点的日志信息上传到Watero Center

## 系统架构

![avatar](http://baidu.com/pic/doge.png)
* 基于Flask实现HTTP RESTful API接口, 作为数据通道
* 基于Socket实现RFC 6455 WebSocket协议, 作为控制通道

## 如何使用

### 环境配置

* Python 3.4
* MySQL 5.7

### 依赖配置

* flask
* falsk-restful
* flask-sqlalchemy
* pymysql

### 开启服务

* 配置Watero Center所连接的MySQL数据库信息
* 配置HTTP RESTful API服务和WebSocket服务绑定的主机地址和端口号
