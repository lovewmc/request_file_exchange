import logging


def get_request_log(result):
    """
    服务获得请求
    :param result:
    :return:
    """
    log = logging.getLogger('get_request_log')
    log.info(result)


def write_file_log(result):
    """
    异步任务写文件时，记录写文件的日志信息
    :param result:
    :return:
    """
    log = logging.getLogger('write_file_log')
    log.info(result)


def read_target_file_log(result):
    """
    读文件时，记录读文件的日志信息
    :param result:
    :return:
    """
    log = logging.getLogger('read_target_file_log')
    log.info(result)


def send_request_log(result):
    """
    文件转成请求后，发送请求时，记录发送请求的日志信息
    :param result:
    :return:
    """
    log = logging.getLogger('send_request_log')
    log.info(result)
