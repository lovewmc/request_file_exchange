import datetime
import json
import os
import shutil
import requests
from celery import shared_task

from Exchange.views.dao.DomainDao import get_domain_obj
from Exchange.views.dao.RequestHistoryDao import read_request_order, return_request_order
from Exchange.views.service.RecordLog import read_target_file_log, send_request_log
from request_file_exchange import settings
from json import JSONDecodeError


@shared_task(name='traversal_dir')
def traversal_dir():
    file_route_list = all_path(settings.READ_PATH)
    if file_route_list:
        for file_route in file_route_list:
            if file_route.endswith(settings.FILE_POSTFIX):
                read_target_file.delay(file_route)


@shared_task(name='read_target_file')
def read_target_file(file_route):
    """
    将源目录中的文件存进新的目录中，并读取新文件的内容
    :param file_route: 源目录中文件的路径
    :return:
    """
    file_name = file_route.split('/')[-1]
    unique_code = file_name.split('.')[0]

    new_file_route = os.path.join(settings.TARGET_PATH, file_name)
    # 如果新的目录中已经存在源目录中的文件，则删除源目录中的文件，如果不存在则将源目录中的文件删除并移动到新目录下
    if os.path.isfile(new_file_route):
        if os.path.isfile(file_route):
            os.remove(file_route)
    else:
        # 将源目录中的该文件移动到指定的新目录下
        shutil.move(file_route, settings.TARGET_PATH)
    with open(new_file_route, 'r') as f:
        file_data = f.read()
        # 读取文件时，将更新的数据存进数据库中
        read_request_order(unique_code, datetime.datetime.now(), file_data)
        send_request.delay(file_data, unique_code, new_file_route)

    log_info = '  源目录文件：' + file_route + '  新目录文件：' + new_file_route + '  读取的数据：' + file_data
    read_target_file_log(log_info)


@shared_task(name='send_request', bind=True, max_retries=10, retry_backoff=5, retry_jitter=False,
             autoretry_for=(Exception, JSONDecodeError, ConnectionError), )
def send_request(self, file_data, unique_code, new_file_route):
    """
    发送请求，删除新目录中的文件，并更新数据库
    :param self:
    :param file_data: 文件中的content数据
    :param identity_code: 文件名
    :param new_file_route: 新文件的路径
    :return:
    """
    file_content = json.loads(file_data)
    log_info = '文件内容：' + file_data
    if file_content:
        request_url = file_content.get('request_url')
        request_body = file_content.get('request_body')
        request_body['return_flag'] = unique_code.split('_')[-1]
        method = file_content.get('method').lower()
        domain_name = request_url.split('/')[2]
        domain_obj = get_domain_obj(domain_name)
        if domain_obj:
            request_url = request_url.replace(domain_name, domain_obj.ip)
        else:
            log_info += ('  请求url：' + request_url + '--域名错误')
            send_request_log(log_info)
            raise Exception("域名错误")
        if method == 'post':
            try:
                re = requests.post(request_url, json=request_body, timeout=20)
            except:
                log_info += ('  请求url：' + request_url + '  请求体：' + json.dumps(request_body) + '--post方法连接超时')
                send_request_log(log_info)
                raise Exception("连接超时")
        elif method == 'get':
            try:
                re = requests.get(request_url, params=request_body, timeout=20)
            except:
                log_info += ('  请求url：' + request_url + '  请求体' + json.dumps(request_body) + '--get方法连接超时')
                send_request_log(log_info)
                raise Exception("连接超时")
        else:
            log_info += ('  请求url：' + request_url + '--请求方法错误')
            send_request_log(log_info)
            raise Exception("请求方法错误")
        if re.text != 'success':
            # 发请求失败
            log_info += ('  请求url：' + request_url + '--返回结果不正确')
            send_request_log(log_info)
            raise Exception("返回结果不正确")
        else:
            # 发请求成功
            os.remove(new_file_route)
            return_request_order(unique_code, datetime.datetime.now())

        log_info = '  文件内数据：' + file_data + '  请求url：' + request_url + '  返回结果：' + re.text

    send_request_log(log_info)


def all_path(dirname):
    result = []  # 所有的文件
    for maindir, subdir, file_route_list in os.walk(dirname):
        for filename in file_route_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            result.append(apath)
    return result
