import json

from comk_django_account.models import Account
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class AddAccount(View):
    """
    添加应用账户
    """

    def post(self, request):
        request_data = json.loads(request.body)
        aa = Account()
        aa.SaveTag = True
        aa.description = request_data.get('description')
        aa.is_use = True
        aa.appid = request_data.get('appid')
        aa.pri_key = request_data.get('pri_key')
        aa.own_public_key = request_data.get('own_public_key')
        aa.other_public_key = request_data.get('other_public_key')
        aa.save()
        return HttpResponse("success")