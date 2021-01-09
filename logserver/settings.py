"""
    Copyright (C) 2020  OpenModelRailRoad, Florian Thiévent

    This file is part of "OMRR".

    "OMRR" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "OMRR" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys

from decouple import config, Csv
from dj_database_url import parse as db_url
from django.contrib.messages import constants as messages

# OMRR Settings
WSGI_APPLICATION = 'logserver.wsgi.application'

INSTALLED = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

CONSOLE_RECONNECT_INTERVALL = 5000
CONSOLE_RECONNECT_ATTEMPTS = 'null'
SNIFFER_MISSED_HEARTBEATS = 2
SNIFFER_CONNECT_TO_PORT = 11337
SNIFFER_MANAGER_THREAD_NAME = 'sniffer-manager-thread'
SNIFFER_SERVER_THREAD_NAME = 'sniffer-server-thread'
MESSAGE_PUSHER_THREAD_NAME = 'message-pusher-thread'
MESSAGE_RETENTION_TIME = 86400

WS_URI = 'ws://127.0.0.1:8000/ws/console/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third Party Packages
    'channels',
    'django_q',

    # Application Packages
    'appsettings',
    'console',
    'logsearch',
    'railmessages',
    'sniffer',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'logserver.urls'

TEMPLATES = [
    {'BACKEND': 'django.template.backends.django.DjangoTemplates',
     'DIRS': [os.path.join(BASE_DIR, 'templates')],
     'APP_DIRS': True,
     'OPTIONS': {
         'context_processors': [
             'django.template.context_processors.debug',
             'django.template.context_processors.request',
             'django.contrib.auth.context_processors.auth',
             'django.contrib.messages.context_processors.messages',
         ],
     },
     },
]

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite://./db.sqlite3',
        cast=db_url
    )
}
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'de-CH'
TIME_ZONE = 'Europe/Zurich'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
LOGIN_REDIRECT_URL = '/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



# Django Q Cluster
Q_CLUSTER = {
    'name': 'omrr-logserver',
    'workers': 10,
    'timeout': 60,
    'retry': 120,
    'queue_limit': 500,
    'bulk': 50,
    'orm': 'default',
    'save_limit': 250,
    'guard_loop': 30
}
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logserver.console': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(asctime)s %(levelname)s: %(threadName)s %(name)s %(message)s',
        },
        'logserver.file': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '%(asctime)s %(levelname)s: %(threadName)s %(name)s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'logserver.console',
            'stream': sys.stdout
        },
        'django.console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'logserver.console',
            'stream': sys.stdout
        },
        'qconsole': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'logserver.console',
            'stream': sys.stdout
        },
        'logserver-file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/log/omrr-logserver.log",
            'maxBytes': 500000,
            'backupCount': 5,
            'formatter': 'logserver.file',
        },

    },
    'loggers': {
        'logserver': {
            'handlers': ['console', ],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django-q': {
            'handlers': ['qconsole', ],
            'level': 'DEBUG',
        },
    }

}

# Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
ASGI_APPLICATION = 'logserver.asgi.application'