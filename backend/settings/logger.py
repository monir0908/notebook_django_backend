import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'notebook-error.log',
            'maxBytes': 1024*1024*100,  # 5MB
            'backupCount': 5,
            'level': 'ERROR',
            'formatter': 'standard',
        },
    },
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}




# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'root': {
#         'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
#         'handlers': ['console'],
#     },
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                       '%(process)d %(thread)d %(message)s',
#         },
#         'aws': {
#             'format': '%(levelname)s %(asctime)s %(module)s '
#                       '%(process)d %(thread)d %(message)s',
#             'datefmt': "%Y-%m-%d %H:%M:%S",
#         }
#     },
#     'handlers': {
#         'console': {
#             'level':  os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG'),
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG'),
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'django': {
#             'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
#             'handlers': ['console'],
#             'propagate': False,
#         },
#         'django.request': {
#             'handlers': ['console'],
#             'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
#             'propagate': False,
#         },
#     },
# }