from django.conf.urls import url

from Exchange.views.Gateway import GatewayDo

urlpatterns = [
    url(r'^gateway/',GatewayDo.as_view(),name = '接口服务'),
]