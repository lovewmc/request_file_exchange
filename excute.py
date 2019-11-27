import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "request_file_exchange.settings")
django.setup()  # 加载django程序
from Exchange.models import RequestHistoryOrder

import datetime

if __name__ == '__main__':
    unique_code = '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    request_obj, flag = RequestHistoryOrder.objects.get_or_create(unique_code=unique_code)
