import datetime
import json
import os
import random
from json import JSONDecodeError

from celery import shared_task, app

from Exchange.views.dao.RequestHistoryDao import create_request_order
from Exchange.views.service.RecordLog import write_file_log
from request_file_exchange import settings


@shared_task(name='write_file', bind=True, max_retries=10, retry_backoff=5, retry_jitter=False,
             autoretry_for=(Exception, JSONDecodeError, ConnectionError), )
def write_file(self, content, file_name):
    log_info = '文件内容：' + str(content) + '  文件名：' + str(file_name)
    try:
        file_route = os.path.join(settings.BASE_DIR, 'file', file_name)
        with open(file_route, 'w') as f:
            f.write(json.dumps(content))
            create_file_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            create_request_order(file_name, datetime.datetime.now())
            log_info += ('  写入时间：' + create_file_time)
        write_file_log(log_info)
    except:
        log_info = '文件写入错误 ：文件内容：' + str(content) + '  文件名：' + str(file_name)
        write_file_log(log_info)
        raise Exception("--写文件错误")
