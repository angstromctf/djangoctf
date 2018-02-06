SECRET_KEY = '[REDACTED]'
DEBUG = False

ALLOWED_HOSTS = ['api.angstromctf.com', 'localhost']

START_TIME = '2017-03-25 12:00:00-04'
END_TIME = '2017-04-01 12:00:00-04'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'angstromctf',
        'USER': 'djangoctf',
        'PASSWORD': '[REDACTED]',
        'HOST': 'localhost',
        'PORT': ''
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SHELL_ENABLED = True
SHELL_PRIVATE_KEY = "djangoctf/shell_privkey"
SHELL_HOSTNAME = "shell.angstromctf.com"

REQUIRE_USER_ACTIVATION = True

EMAIL_HOST = 'smtp.someserver.com'
EMAIL_HOST_USER = '[REDACTED]'
EMAIL_HOST_PASSWORD = '[REDACTED]'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'angstromCTF Team <contact@angstromctf.com>'
DEFAULT_FROM_EMAIL = 'angstromCTF Team <contact@angstromctf.com>'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/djangoctf.log'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

ADMINS = [('Admin', 'admin@angstromctf.com')]
