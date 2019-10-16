import base64
import json

import rsa
from alipay.aop.api.constant.CommonConstants import PYTHON_VERSION_3
from alipay.aop.api.util.SignatureUtils import fill_private_key_marker, fill_public_key_marker


def get_sign_content(all_params):
    """
    将键值对数据构造为待签名的字符串

    示例语言是Python，仅供参考。

    :param all_params: 键值对数据
    :return:
    """
    sign_content = ""
    for (k, v) in sorted(all_params.items()):  # 按键进行字典排序
        value = v
        if not isinstance(value, str):  # 如果值不为字符串
            value = json.dumps(value, ensure_ascii=False)  # 则将值转变为json字符串
        sign_content += ("&" + k + "=" + value)  # 拼接规则
    sign_content = sign_content[1:]
    return sign_content


def sign_with_rsa2(private_key, sign_content, charset):
    """
    签名方法

    示例语言是Python，仅供参考。

    :param private_key: 私钥
    :param sign_content: 待签名串
    :param charset: 编码格式
    :return:
    """
    if PYTHON_VERSION_3:
        sign_content = sign_content.encode(charset)
    private_key = fill_private_key_marker(private_key)
    signature = rsa.sign(sign_content, rsa.PrivateKey.load_pkcs1(private_key, format='PEM'), 'SHA-256')
    sign = base64.b64encode(signature)
    if PYTHON_VERSION_3:
        sign = str(sign, encoding=charset)
    return sign


def verify_with_rsa(public_key, message, sign):
    """
    验签方法

    示例语言是Python，仅供参考。

    :param public_key: 公钥
    :param message: 待验签串(需转换为bytes数组)
    :param sign: 签名
    :return:
    """
    public_key = fill_public_key_marker(public_key)
    sign = base64.b64decode(sign)
    return bool(rsa.verify(message, sign, rsa.PublicKey.load_pkcs1_openssl_pem(public_key)))

if __name__ == '__main__':
    data = {
        "appid": "3817407951",
        "method": "request_file_server.request.to.file",
        "timestamp": '2018-09-13 09:49:08',
        "content": {
            "method": "post",
            "request_url": "www.baidu.com",
            "request_body":
                {
                    "identity_code": "ding123",
                    'back_url': 'www.google.com'
                }
        },
    }

    # data = {"a": "123", "b": "456", "c": {"d": "789"}}
    private_key = 'MIIEowIBAAKCAQEAw2trVpIaMbXjD72Hm8ZylSqJ+UG6nbEf7lhhKvurq+l0XhrFlls6h9PfbW2R5i5XOV4ptnn/zhpD8uwUJjgIYYj0s+UNqNj9Aa8dGXM8Ebav1ph1r7eZ7ibWpM9mzT3l1LucqaBzciDPuv4cA+inulR/CAByZYbkzb+aHQvDOZk77gZyvLMcqAlfg8pjAmDdkseDIBGawbbY7pOQ/ZawmwcGAFjBEAzq1e8em/PM3coKil3sogoIEoNCQBliL5iTMXXcUQn8NzGVVxVjPUyRawmsGiNJev+RyqEA3NWiRNV8a1jqVdz2cs/kLUtxiBOzDvQi1qu+ARMF6u2fUg6hRwIDAQABAoIBAGbuteMrodB9VdR8qGlM5h3cAkDgdkOJgKAyvTu+xHYQydKnl1vTQck5uH4TML5lulvlVWNgb3VIMHJMF3DqIr/9O6dmBwPhB6NTcahuIj3SVFxcgeDEfLgMjRLSi/uflueuyp4ufaCn18NPBcKpUW+8Ag1c7uS7YNlfCvYxs+sp9oNFXdZVrZ4m6CeXQzjh8ALNstjBW4jg2d1GQXO3TCPFwfDTEWvXm8Maz25HEtotHLX5yyqFqix17lt6QVc4KBWKi1/Du399V64j9aaEMbdeiSYNhq+MLOm6Hj8D6w2wJPVlO4ZBZj/g+Hd2hOwAjb2rfBgWXFif8mkw2aJSm8ECgYEA+P889rfyAG1e6Z0l9fzuT++PCLnPw+zMUBntU/K2HbAMrxsGb9yOG4+E7djMPSPw6jmFCL8vNiT5qoy7dXudYpobIf4qZDhV4Hkm1/11ZKVwLi+6kq7aeCxcwclzZMwxWlJKxE7mungdRyu4RgB0STEGwIdloKbWdssr32KNxZsCgYEAyOptZjfAEofCNEufa+SZ0l0Ne5jzjchOXPEgOeIsN9Ol35kMSyhktVQhUSW1lYfk8NSgKgoBSf3pRIMwJaWc3RMXzJRgySeNCzj5IrH5SWadG2Wzyb6oAPQP3CrrvzWi3iBWG0NSN+99klLrxgBBTnh3qhHpHWtZudTrjhOaQ8UCgYEA3bPdo0u7dXfsp5OeBj3UL2Z88+cGQEwqyzOapkGYuCxVzuAARj+aZJ3QXTrI97N1wge/FT+tmMcpahrumrebNf1DJWw6cIvcowccd/qcuSW5Eda7h/maWqAdYwqs7VYGp4ZYPhyGwgdLAmDCLcofwD+f5HNqILYMhS93++mzk/sCgYAs/GB2bLEy9PbE4tHVRKA0e+VS8VJHQrxZDxxaGYwxC9CuGgSop2i1ORskoj7gNkdKrTEXeJoFSTb7wiv7ofNXhLjlc6ugHpz0EFOoMxVQHAu9YK4609emLv+GGo4iiA3pkm/1NsOoBpWlN6/W66OzwEF68PuzPKAgfc4oR7dYyQKBgG9ZkAgCD/mA4pueCkGZntqcQISdpELw7zzTD0DtWNVI1q6Lwc59VVdkGU5EuIMkSxW/Pi0XaYazepO8TRLRcDWGgKco9w1iFqlgFuXIBVd2pWRxhAp1PChhP7yQ6HPgJlGKJeqc6ClL2sGKWJue9hH3niZv/+ayHgHRQll5SqiN'
    t = get_sign_content(data)
    tt = sign_with_rsa2(private_key, t, 'utf-8')
    print("tt = ", tt)

    # public_key = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw2trVpIaMbXjD72Hm8ZylSqJ+UG6nbEf7lhhKvurq+l0XhrFlls6h9PfbW2R5i5XOV4ptnn/zhpD8uwUJjgIYYj0s+UNqNj9Aa8dGXM8Ebav1ph1r7eZ7ibWpM9mzT3l1LucqaBzciDPuv4cA+inulR/CAByZYbkzb+aHQvDOZk77gZyvLMcqAlfg8pjAmDdkseDIBGawbbY7pOQ/ZawmwcGAFjBEAzq1e8em/PM3coKil3sogoIEoNCQBliL5iTMXXcUQn8NzGVVxVjPUyRawmsGiNJev+RyqEA3NWiRNV8a1jqVdz2cs/kLUtxiBOzDvQi1qu+ARMF6u2fUg6hRwIDAQAB'
    # # message = json.dumps(data)
    #
    # data = t.encode('utf-8')
    #
    # a = verify_with_rsa(public_key, data, tt)
    # print(a)