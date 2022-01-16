from .base import *


DEBUG = False

# ALLOWED_HOSTS = env.list('pro_ALLOWED_HOSTS')
ALLOWED_HOSTS = ['45.76.97.82', 'localhost']

DATABASES = {
    'default': env.db(),
}


STATIC_ROOT = BASE_DIR / 'static'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# ロギング設定
#ログ出力先のディレクトリを設定する
LOG_BASE_DIR = os.path.join("/var", "log", "app")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(asctime)s [%(levelname)s] %(message)s"}},
    "handlers": {
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "info.log"),
            "formatter": "simple",
        },
        "warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "warning.log"),
            "formatter": "simple",
        },
        "error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_BASE_DIR, "error.log"),
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["info", "warning", "error"],
        "level": "INFO",
    },
}