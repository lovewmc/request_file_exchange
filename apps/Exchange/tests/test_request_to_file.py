import base64
import json
import os
import django
# 配置django的setting文件
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "request_file_exchange.settings")
# 加载django程序
django.setup()

from django.test import Client
from django.conf import settings
from Exchange.tests.varify_sign import get_sign_content, sign_with_rsa2

# 构造Client，一个全局变量
c = Client()


class APITests():
    """
    这里应为需要用到原数据库的数据，因此，不继承TestCase
    """

    def test_gataway(self, data, url):
        """
        测试 /province_server/gateway/
        预期 :
        :param data:
        :return:
        """

        # 每一组data都是一个测试用例
        if not data:
            data = {'method': 'test'}
        # 因为项目的API接收的是json字符串，因此需要进行一次转化
        json_data = json.dumps(data)
        # 注意设置content_type类型
        response = requests.post(url=url, json=data)
        # response = c.post(url, json_data, content_type='application/json')
        return response


def main_t(data, url):
    """
    使用django的测试模块进行测试
    :param data:
    :return:
    """

    api_t = APITests()

    # 运行测试程序
    result = api_t.test_gataway(data, url)

    print('--------------------')
    print(result.text)
    print(result)
    # assert result['code'] == '1000', '结果错误，返回码不是1000'
    print('--------------------')


def get_sign():
    data = {
        "appid": "3817407951",
        "method": "request_file_server.request.to.file",
        "timestamp": '2018-09-13 09:49:08',
        "content": {
            "method": "post",
            "request_url": "http://qinlan.nat300.top/send_inside/get_response/",
            "return_flag": '',
            "request_body":
                {
                    "identity_code": "ding123456",
                    'back_url': 'http://n8xvp4.natappfree.cc/send_outside/get_data/'
                }
        },
    }

    private_key = 'MIIEowIBAAKCAQEAw2trVpIaMbXjD72Hm8ZylSqJ+UG6nbEf7lhhKvurq+l0XhrFlls6h9PfbW2R5i5XOV4ptnn/zhpD8uwUJjgIYYj0s+UNqNj9Aa8dGXM8Ebav1ph1r7eZ7ibWpM9mzT3l1LucqaBzciDPuv4cA+inulR/CAByZYbkzb+aHQvDOZk77gZyvLMcqAlfg8pjAmDdkseDIBGawbbY7pOQ/ZawmwcGAFjBEAzq1e8em/PM3coKil3sogoIEoNCQBliL5iTMXXcUQn8NzGVVxVjPUyRawmsGiNJev+RyqEA3NWiRNV8a1jqVdz2cs/kLUtxiBOzDvQi1qu+ARMF6u2fUg6hRwIDAQABAoIBAGbuteMrodB9VdR8qGlM5h3cAkDgdkOJgKAyvTu+xHYQydKnl1vTQck5uH4TML5lulvlVWNgb3VIMHJMF3DqIr/9O6dmBwPhB6NTcahuIj3SVFxcgeDEfLgMjRLSi/uflueuyp4ufaCn18NPBcKpUW+8Ag1c7uS7YNlfCvYxs+sp9oNFXdZVrZ4m6CeXQzjh8ALNstjBW4jg2d1GQXO3TCPFwfDTEWvXm8Maz25HEtotHLX5yyqFqix17lt6QVc4KBWKi1/Du399V64j9aaEMbdeiSYNhq+MLOm6Hj8D6w2wJPVlO4ZBZj/g+Hd2hOwAjb2rfBgWXFif8mkw2aJSm8ECgYEA+P889rfyAG1e6Z0l9fzuT++PCLnPw+zMUBntU/K2HbAMrxsGb9yOG4+E7djMPSPw6jmFCL8vNiT5qoy7dXudYpobIf4qZDhV4Hkm1/11ZKVwLi+6kq7aeCxcwclzZMwxWlJKxE7mungdRyu4RgB0STEGwIdloKbWdssr32KNxZsCgYEAyOptZjfAEofCNEufa+SZ0l0Ne5jzjchOXPEgOeIsN9Ol35kMSyhktVQhUSW1lYfk8NSgKgoBSf3pRIMwJaWc3RMXzJRgySeNCzj5IrH5SWadG2Wzyb6oAPQP3CrrvzWi3iBWG0NSN+99klLrxgBBTnh3qhHpHWtZudTrjhOaQ8UCgYEA3bPdo0u7dXfsp5OeBj3UL2Z88+cGQEwqyzOapkGYuCxVzuAARj+aZJ3QXTrI97N1wge/FT+tmMcpahrumrebNf1DJWw6cIvcowccd/qcuSW5Eda7h/maWqAdYwqs7VYGp4ZYPhyGwgdLAmDCLcofwD+f5HNqILYMhS93++mzk/sCgYAs/GB2bLEy9PbE4tHVRKA0e+VS8VJHQrxZDxxaGYwxC9CuGgSop2i1ORskoj7gNkdKrTEXeJoFSTb7wiv7ofNXhLjlc6ugHpz0EFOoMxVQHAu9YK4609emLv+GGo4iiA3pkm/1NsOoBpWlN6/W66OzwEF68PuzPKAgfc4oR7dYyQKBgG9ZkAgCD/mA4pueCkGZntqcQISdpELw7zzTD0DtWNVI1q6Lwc59VVdkGU5EuIMkSxW/Pi0XaYazepO8TRLRcDWGgKco9w1iFqlgFuXIBVd2pWRxhAp1PChhP7yQ6HPgJlGKJeqc6ClL2sGKWJue9hH3niZv/+ayHgHRQll5SqiN'
    t = get_sign_content(data)
    sign = sign_with_rsa2(private_key, t, 'utf-8')
    return sign, data


def test_request_to_file():
    sign, data = get_sign()
    data['sign'] = sign
    url = "http://192.168.1.117:8000/request_file_exchange/gateway/"
    main_t(data, url)


if __name__ == '__main__':
    test_request_to_file()
