SECRET_KEY = '[REDACTED]'
DEBUG = True
ALLOWED_HOSTS = []

import os
from djangoctf.settings import BASE_DIR

START_TIME = '2017-03-25 12:00:00-04'
END_TIME = '2017-04-01 12:00:00-04'

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

SHELL = {
    'enabled': False
}

REQUIRE_USER_ACTIVATION = False
