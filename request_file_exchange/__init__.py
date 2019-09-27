from __future__ import absolute_import,unicode_literals
from request_file_exchange.set_conf.celery import app as celery_app

# 确保django启动的时候这个app能够被加载到
__all__ = ['celery_app']