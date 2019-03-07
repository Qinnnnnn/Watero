# Watero Center

![](https://img.shields.io/badge/version-1.0-orange.svg)
[![](https://img.shields.io/github/license/Qinnnnnn/Watero_Center.svg)](https://github.com/Qinnnnnn/Watero_Center/blob/master/LICENSE)
![](https://img.shields.io/badge/python-3.7-blue.svg)
* Watero Center是一项数据接收、转发和投递集成服务
* [Watero Go](https://github.com/Qinnnnnn/Watero_Go)是部署于服务器与Watero Center通信的Agent服务，用于采集节点数据并上报Watero Center，同时接收Watero Center主动推送的信息

## 系统架构

![image](http://ww1.sinaimg.cn/mw690/a1bd622cgy1g0uphyspbzj20hq0kmt95.jpg)
* 基于Flask实现RESTful API服务，作为单向数据通道
* 基于Socket TCP实现WebSocket服务，遵守IETF RFC 6455协议规范，作为双向数据通道
* RESTful API服务和WebSocket服务数据互通

## 开发配置

#### 开发环境

* Python 3.7
* MySQL 5.7

#### 依赖库

* flask
* flask-restful
* flask-sqlalchemy
* pymysql

#### 开启服务

1. 配置MySQL数据库IP地址和端口
2. 配置RESTful API服务和WebSocket服务的IP地址和端口
3. 启动服务

## 生产配置

#### Docker部署

1. 构建Docker镜像，指定RESTful API服务和WebSocket服务的端口映射
2. 启动镜像

## 文档

请参考GitHub Wiki


