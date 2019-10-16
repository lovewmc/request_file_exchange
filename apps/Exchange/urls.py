from django.conf.urls import url

from Exchange.views.Gateway import GatewayDo
from Exchange.views.service.AddAccount import AddAccount

urlpatterns = [
    url(r'^gateway/',GatewayDo.as_view(),name = '接口服务'),
    url(r'^add_account/',AddAccount.as_view(),name = '添加账户')
]