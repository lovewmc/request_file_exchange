from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "request_file_exchange.settings")
from datetime import timedelta
from celery import Celery

app = Celery('request_file_exchange')
# 自动发现模块下tasks.py文件中的任务
app.autodiscover_tasks()

# celery配置
# 使用redis作为任务中间人
app.conf.broker_url = 'redis://{}:{}/0'.format(settings.REDIS_HOST, settings.REDIS_PORT)
# 任务结果存储区，值为'django-db'，那么必须启用django-celery-results
app.conf.result_backend = 'django-db'
# app.conf.result_backend = 'redis://{}:{}/1'.format(settings.REDIS_HOST, settings.REDIS_PORT)
# 任务结果的序列化方式
app.conf.result_serializer = 'json'
# 每个worker执行了多少任务会死掉
app.conf.worker_max_tasks_per_child = 40
# 设置时区，与django相同
app.conf.timezone = settings.TIME_ZONE
# 是否启用utc，与Django相同即可
app.conf.enable_utc = settings.TIME_ZONE

app.conf.result_expires = 20


# celery定时配置
app.conf.beat_schedule = {
    'beat_for_traversal': {  # 任务名，可自定义
        'task': 'traversal_dir',  # 需要加载的异步函数
        'schedule': 2,
        'args': (),  # 函数位置参数
        'kwargs': {},  # 函数关键字参数
    },
}
