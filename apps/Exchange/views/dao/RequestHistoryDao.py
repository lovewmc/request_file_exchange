import json

from Exchange.models import RequestHistoryOrder


def received_request_order(identity_code, request_body, file_name, request_time):
    """
    接收到请求后对请求记录表进行的操作
    :param content:
    :param file_name:
    :param request_time:
    :return:
    """
    request_obj = RequestHistoryOrder()
    request_obj.file_id = file_name
    request_obj.identity_code = identity_code
    request_obj.data = request_body
    request_obj.received_time = request_time
    request_obj.status = '1'
    request_obj.save()


def create_request_order(file_name, create_file_time):
    """
    生成文件之后对请求记录表进行的操作
    :param create_file_time:
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(file_id=file_name)
    if not flag:
        request_obj.create_file_time = create_file_time
        request_obj.status = '2'
        request_obj.save()


def read_request_order(file_name, read_file_time):
    """
    读取文件后对请求记录表进行的操作
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(file_id=file_name)
    if not flag:
        request_obj.read_file_time = read_file_time
        request_obj.status = '3'
        request_obj.save()


def return_request_order(file_name,return_time):
    """
    返回结果后对请求记录表进行的操作
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(file_id=file_name)
    if not flag:
        request_obj.return_time = return_time
        request_obj.status = '4'
        request_obj.finish_tag = True
        request_obj.save()
