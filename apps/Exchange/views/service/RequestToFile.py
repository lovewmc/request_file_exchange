import datetime
import json
import random

from Exchange.tasks.task_write_file import write_file
from Exchange.views.dao.RequestHistoryDao import received_request_order
from Exchange.views.service.RecordLog import get_request_log
from Exchange.views.service.ServiceMoudel import ServiceMoudel


class RequestToFile(ServiceMoudel):
    """
    请求转文件
    """

    def deal_request(self):
        """

        :return:
        """
        content = self.content
        request_body = content.get('request_body')
        identity_code = request_body.get('identity_code')

        # 生成文件名
        request_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnm', 6))
        # TODO
        if not identity_code:
            return self.build_error_response_data(msg='identity_code不能为空')
        file_name = identity_code + '_' + request_time + '_' + random_str + '.httpio'
        # 记录日志
        info_log = '文件名：' + file_name
        if content:
            info_log += ('  请求内容：' + str(content))
        get_request_log(info_log)

        # 将请求数据存进数据表中
        received_request_order(identity_code, str(content), file_name, datetime.datetime.now())
        # 异步任务将请求转换成文件
        write_file.delay(content, file_name)
        return self.build_success_response_data(response_data='success', timestamp_now=True)
