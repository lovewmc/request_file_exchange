from django.conf import settings

import datetime

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'read_target_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/read_target_file.log',
            'maxBytes': 1024 * 1024 * 100,  # 100M
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'write_file':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/write_file.log',
            'maxBytes': 1024 * 1024 * 100,  # 100M
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'send_request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/send_request.log',
            'maxBytes': 1024 * 1024 * 100,  # 100M
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'get_request': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/get_request.log',
            'maxBytes': 1024 * 1024 * 100,  # 100M
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'read_target_file_log': {
            'handlers': ['read_target_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'write_file_log':{
            'handlers': ['write_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'send_request_log': {
            'handlers': ['send_request'],
            'level': 'INFO',
            'propagate': True,
        },
        'get_request_log': {
            'handlers': ['get_request'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
