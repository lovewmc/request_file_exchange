from __future__ import absolute_import

from django_celery_results.models import TaskResult

import xadmin
from Exchange.models import DomainOrder, RequestHistoryOrder


class DomainOrderAdmin(object):
    list_display = ('domain_name', 'ip', 'create_time', 'modify_time', 'kind')
    search_fields = ('domain_name', 'ip')
    list_filter = ('create_time', 'modify_time', 'kind')


xadmin.site.register(DomainOrder, DomainOrderAdmin)


class RequestHistoryOrderAdmin(object):
    list_display = (
        'file_id', 'identity_code', 'data', 'received_time', 'create_file_time', 'read_file_time', 'return_time',
        'status',
        'finish_tag')
    list_filter = ('status', 'finish_tag', 'received_time', 'create_file_time', 'read_file_time', 'return_time')
    search_fields = ('identity_code',)


xadmin.site.register(RequestHistoryOrder, RequestHistoryOrderAdmin)


class TaskResultAdmin(object):
    list_display = (
        'task_id', 'task_name', 'date_done', 'status', 'result'
    )
    list_filter = (
        'status', 'date_done', 'task_name'
    )
    search_fields = (
        'task_name', 'task_id', 'status'
    )


xadmin.site.register(TaskResult, TaskResultAdmin)
