import datetime
import json
import os
from json import JSONDecodeError

from celery import shared_task

from Exchange.views.dao.RequestHistoryDao import create_request_order
from Exchange.views.service.RecordLog import write_file_log
from request_file_exchange import settings


@shared_task(name='write_file', bind=True, max_retries=10, retry_backoff=5, retry_jitter=False,
             autoretry_for=(Exception, JSONDecodeError, ConnectionError), )
def write_file(self, content, unique_code, write_flag=True):
    file_name = str(unique_code) + '.httpio'
    log_info = '文件内容：' + json.dumps(content) + '  文件名：' + str(unique_code)
    try:
        if write_flag:
            file_route = os.path.join(settings.WRITE_PATH, file_name)
            with open(file_route, 'w') as f:
                f.write(json.dumps(content))
                create_file_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 写入文件完成后，记录到数据表中
                create_request_order(unique_code, datetime.datetime.now())
                log_info += ('  写入时间：' + create_file_time)
        else:
            # TODO ftp上传文件
            # 请求直接变成字节流通上传一个文件名，ftp接收到会自己写文件
            pass
        write_file_log(log_info)
    except:
        log_info = '文件写入错误 ：文件内容：' + json.dumps(content) + '  文件名：' + unique_code
        write_file_log(log_info)
        raise Exception("--写文件错误")
