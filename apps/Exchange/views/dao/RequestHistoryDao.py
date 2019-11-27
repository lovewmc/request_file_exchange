from Exchange.models import RequestHistoryOrder
from Exchange.views.service.RecordLog import read_target_file_log


def received_request_order(identity_code, unique_code,content, request_time, response_data):
    """
    接收到请求后对请求记录表进行的操作
    :param content:
    :param file_name:
    :param request_time:
    :return:
    """
    # 无论是符合条件的重发请求还是新的请求重发，都需要存进这些数据
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(unique_code=unique_code)

    request_obj.identity_code = identity_code
    request_obj.request_data = content
    request_obj.received_time = request_time
    request_obj.response_data = response_data
    request_obj.write_status = '1'
    if not request_obj.read_file_time:
        request_obj.request_flag = '1'
    else:
        request_obj.request_flag = '2'

    request_obj.save()
    return unique_code


def create_request_order(unique_code, create_file_time):
    """
    生成文件之后对请求记录表进行的操作
    :param create_file_time:
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(unique_code=unique_code)
    if not flag:
        request_obj.create_file_time = create_file_time
        request_obj.write_status = '2'
        if request_obj.read_status == '2':
            request_obj.finish_tag = True
        request_obj.save()


def read_request_order(unique_code, read_file_time, request_data):
    """
    读取文件后对请求记录表进行的操作
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(unique_code=unique_code)

    request_obj.read_file_time = read_file_time
    request_obj.request_data = request_data
    request_obj.read_status = '1'
    if not request_obj.received_time:
        request_obj.request_flag = '2'
    else:
        request_obj.request_flag = '1'
    info_log = '读文件 -------- 文件名：' + unique_code + 'read_status' + request_obj.read_status + 'request_data' + str(
        request_obj.request_data)
    read_target_file_log(info_log)
    request_obj.save()


def return_request_order(unique_code, return_time):
    """
    返回结果后对请求记录表进行的操作
    :return:
    """
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(unique_code=unique_code)
    if not flag:
        request_obj.return_time = return_time
        request_obj.read_status = '2'
        # 如果写文件也完成了，则代表已完成
        if request_obj.write_status == '2':
            request_obj.finish_tag = True
        request_obj.save()


def tell_identity_code(unique_code):
    """
    判断identity_code在数据库中是否已经存在，且接收请求时间和写入文件时间都已经存在
    :param unique_code:
    :return:
    """
    request_obj = RequestHistoryOrder.objects.filter(unique_code=unique_code)
    # 如果对象已经存在
    if request_obj:
        if request_obj[0].create_file_time and request_obj[0].received_time:
            return False
        else:
            return True
    else:
        return True
