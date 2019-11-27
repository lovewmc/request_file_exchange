import datetime
import json
import random

from Exchange.models import RequestHistoryOrder
from Exchange.tasks.task_write_file import write_file
from Exchange.views.dao.RequestHistoryDao import received_request_order, tell_identity_code
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
        return_flag = content.get('return_flag')
        identity_code = request_body.get('identity_code')

        # 判断identity_code不能为空
        if not identity_code:
            return self.build_error_response_data(msg='identity_code不能为空')
        # 完全请求，不支持重发的接口
        if '.' in identity_code:
            return self.build_error_response_data(msg='identity_code不正确')

        # 记录日志
        info_log = '文件名：' + identity_code
        if content:
            info_log += ('  请求内容：' + json.dumps(content))
        get_request_log(info_log)

        if not return_flag:
            unique_code = identity_code + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            unique_code = identity_code + '_' + return_flag
        # 将请求数据存进数据表中
        received_request_order(identity_code, unique_code,json.dumps(content), datetime.datetime.now(), self.build_success_response_data(response_data='success', timestamp_now=True))
        # 异步任务将请求转换成文件
        # TODO 如果使用ftp上传文件，则需要将write_flag=False
        write_file.delay(content, unique_code)
        return self.build_success_response_data(response_data='success', timestamp_now=True)
