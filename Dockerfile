# Docker基础镜像
FROM python:latest
# Docker镜像元数据
MAINTAINER Clever_Moon <qzr19970105@live.com>
# Docker工作目录
WORKDIR /home/qinzerui/Projects/Watero_Center
# 复制依赖清单至WORKDIR
COPY ./requirements.txt .
# 安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir
# 启动容器
CMD ["sh", "./start_service.sh"]
