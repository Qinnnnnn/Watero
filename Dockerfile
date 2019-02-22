# Docker基础镜像
FROM python:3.7.1-stretch
# Docker镜像元数据
MAINTAINER Clever_Moon <qzr19970105@live.com>
# 指定工作目录
WORKDIR /home/Projects/Watero_Center
# 复制工程到Docker根目录
COPY . .
# 运行命令安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir
# 启动容器
CMD ["gunicorn", "flask_manage:create_app()", "-c", "config/gunicorn_config.py"]
