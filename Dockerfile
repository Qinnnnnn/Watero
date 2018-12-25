# 基础Docker镜像
FROM python
# Docker镜像添加元数据
LABEL maintainer="Clever_Moon qzr19970105@live.com" version="v1.0"
# Docker镜像内服务所监听的端口
EXPOSE 5000
# 指定工作目录
WORKDIR /usr/Projects/Watero_Center
# 复制工程到Docker根目录
COPY ./ /Users/qinzerui/Projects/Watero
# 运行命令安装依赖
RUN pip install --upgrade pip \
    pip install --no-cache-dir -r requirements.txt
# 启动容器
CMD ["gunicorn", "-w4","-b0.0.0.0:5000","\"manage:create_app()\""]
