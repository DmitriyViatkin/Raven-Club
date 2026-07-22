# config/logging_config.py
import os

def get_logging_config(base_dir):
    """
    Возвращает словарь конфигурации LOGGING.
    Принимает BASE_DIR из settings.py для корректного построения путей.
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} [{name}:{lineno}] {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            'src': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }