# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "send_outside.settings")
# django.setup()
from django.conf import settings
import json
import collections
import hashlib
import requests


def getsign(param_dict):
    if param_dict is None:
        return ''
    od = collections.OrderedDict(sorted(param_dict.items()))
    string = dict2str(od)
    string += '&key=12345'
    return SHA256(string)


def dict2str(dictobj):
    if not isinstance(dictobj, dict):
        raise Exception('string')
    return '%s' % '&'.join(['%s=%s' % (k, obj2str(v)) for k, v in dictobj.items()])


def obj2str(obj):
    if isinstance(obj, list):
        return '[%s]' % ','.join(['%s' % obj2str(x) for x in obj])
    elif isinstance(obj, dict):
        return '{%s}' % ','.join(['"%s":"%s"' % (k, v) for k, v in obj.items()])
    else:
        return str(obj)


def SHA256(encrypt_str):
    m = hashlib.sha256()
    m.update(encrypt_str.encode('utf-8'))
    return m.hexdigest().upper()


def requestWrite02c78_Params(request_code, data):
    """
    这里以 【内网侧服务】向 【互联网侧项目】发送请求为例，给出调用示例
    :return:
    """
    inner2internet_parameter = data   # 【内网侧服务】要向【互联网项目推送的数据】
    identity_code = request_code        # 【内网侧服务】的唯一订单标识
    inner_request2file_ip = settings.GZ_URL  # 【内网-请求转文件服务】ip和端口，请写入配置文件，不要像这里一样采用硬编码方式
    inner_request2file_url = 'http://{0}/oi/api/worker/'.format(inner_request2file_ip)         # 拼接【内网-请求转文件服务】地址
    inner_side_url_callback = settings.BACK_URL  # 【内网-文件转请求服务】会将【互联网侧项目】JsonResponse的结果回调给 【内网项目】
    internet_side_url = '/send_inside/get_result/'  # 给出url后面的部分【互联网侧项目】的地址,ip和端口统一由【互联网侧】的nginx服务负责，匹配到该url就转发给某【互联网侧项目】
    data = {
        'method': 'post',                       # 请求的方法，目前统一是post方式
        'request_url': internet_side_url,       # 【内网侧服务】要向【互联网侧项目】项目发送请求时，给出的url部分
        'identity_code': identity_code,         # 【内网侧服务】的唯一订单标识，对于支付可使用订单号
        'back_url': inner_side_url_callback,    # 【内网侧服务】接收【互联网侧项目】返回的结果
        'request_body': json.dumps(inner2internet_parameter),  # 【内网侧服务】向【互联网侧项目】发送的请求数据
    }
    data['sign'] = getsign(data)                # 生成数据校验位，防止人为或者环境引起的数据窜改
    re = requests.post(inner_request2file_url, data=data, timeout=5)
    return re

# if __name__ == '__main__':
#     res = requestWrite02c78_Params('213213', {'code': '1000'})
#     print(res.json())