#!/usr/bin/env bash

# Docker部署服务
sudo docker run -d -p 5000:5000 --name watero-center --restart always -v /home/qinzerui/Projects/Watero_Center:/home/qinzerui/Projects/Watero_Center watero:v1.0