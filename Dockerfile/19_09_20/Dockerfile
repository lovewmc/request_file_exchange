# Update pip requirements for python
# Run cmd
#   docker build -t registry.cn-hangzhou.aliyuncs.com/mengjieguo/trailer_notice:19.07.19_Alpha .
# docker push cmd
#   docker push registry.cn-hangzhou.aliyuncs.com/mengjieguo/trailer_notice:19.07.19_Alpha

FROM registry.cn-hangzhou.aliyuncs.com/mengjieguo/alpine_base:19.05.31_Alpha

COPY requirements.txt /home/docker/code/app/
# 这里修改下，增加删除cache操作
RUN pip3 install -r /home/docker/code/app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple && rm -r /root/.cache
