import logging
from datetime import datetime

from comk_django_plugin import BaseMoudel


class ServiceMoudel(BaseMoudel):
    '''
    所有的服务，都基于该 Moudel 进行开发，并且返回数据的格式，已经固定，即包含字段 code、msg、timestamp。

    '''

    def __init__(self, data=None):
        '''
        数据构建

        '''
        super().__init__()
        # self.data和data为post请求数据，以'method'、'content'、'appid'为键的字典类型
        self.data = data
        if data and isinstance(data, dict):
            self.appid = data.get('appid')
            self.content = data.get('content')

    def params_check(self, params_list):
        '''
        :function:
        必传字段的参数检查
        判断params_list中的每个参数，是否存在content的键对象中

        :param params_list:

        :return:
        如果传递的参数不在content键对象中则返回response_data
        '''

        biz_keys = self.content.keys()
        for param in params_list:
            if param not in biz_keys:
                msg = '{} is not in content，please check the params'.format(param)
                return self.build_return_response_data(code='5001', msg=msg)

    def deal_request(self):
        '''
        必要方法，也是所有服务执行方法，需要被重写

        :return:
        '''
        return self.response_data

