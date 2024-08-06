# 使用官方 Python 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量以防止 Python 生成.pyc 文件
ENV PYTHONUNBUFFERED=1

# 暴露应用运行的端口
EXPOSE 80

# 运行 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
