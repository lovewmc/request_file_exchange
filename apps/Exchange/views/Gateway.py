from comk_django_account.views.utils.app_check import request_to_response
from comk_django_plugin import PublicServer
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from Exchange.views.Funs import FUNCTIONS


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(request_to_response, name='dispatch')
class GatewayDo(View):
    """

    """

    @transaction.atomic
    def post(self, request):
        ps = PublicServer(request)
        request_data = ps.request_data
        method = request_data.get('method')
        if method not in FUNCTIONS.keys():
            result = {'code': '4005', 'msg': '{} 方法不存在，或者尚未支持'.format(method)}
            return result
        else:
            # FUNCTIONS[method]得到的是类名，
            # request_data为初始化类时传入的参数
            # deal_request为类中处理请求的方法
            result = FUNCTIONS[method](request_data).deal_request()
            return result
