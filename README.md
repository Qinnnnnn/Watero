# Watero Center

![](https://img.shields.io/badge/version-1.0-orange.svg)
[![](https://img.shields.io/github/license/Qinnnnnn/Watero_Center.svg)](https://github.com/Qinnnnnn/Watero_Center/blob/master/LICENSE)
![](https://img.shields.io/badge/python-3.7-blue.svg)
* Watero Center是一项数据接收、转发和投递集成服务
* [Watero Go](https://github.com/Qinnnnnn/Watero_Go)是Watero Center部署于服务器的Agent服务，用于采集节点数据并上报Watero Center，同时接收Watero Center推送的控制信息

## 系统架构

![avatar](https://github.com/Qinnnnnn/Watero_Center/blob/master/Watero_Center系统架构.jpg)
* 基于Flask实现HTTP RESTful API接口，作为数据通道
* 基于Socket实现RFC 6455规定的WebSocket协议，作为控制通道

## 如何使用

### 环境配置

* Python 3.4
* MySQL 5.7

### 依赖配置

* flask
* flask-restful
* flask-sqlalchemy
* pymysql

### 开启服务

1. 配置MySQL数据库
2. 配置服务IP地址和端口
3. 开启服务
