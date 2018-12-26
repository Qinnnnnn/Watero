# Docker基础镜像
FROM python:3.7.1-stretch
# Docker镜像元数据
LABEL maintainer="Clever_Moon qzr19970105@live.com" version="v1.0"
# Docker镜像服务暴露端口
EXPOSE 5000
# 复制工程到Docker根目录
COPY . /usr/Projects/Watero_Center
# 指定工作目录
WORKDIR /usr/Projects/Watero_Center
# 运行命令安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir
# 启动容器
CMD ["gunicorn", "-c", "config/gunicorn_config.py", "manage:create_app()"]
