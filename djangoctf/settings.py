"""
Django settings for djangoctf project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import json

# Parse the secure configuration file
with open('djangoctf/settings.json') as config_file:
    config = json.loads(config_file.read())

# Read security options from the file
SECRET_KEY = config['secret_key']
DEBUG = config['debug']
ALLOWED_HOSTS = config['allowed_hosts']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'password_reset',
    'ctfapp',
    'crispy_forms',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangoctf.urls'

WSGI_APPLICATION = 'djangoctf.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'ctfapp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

for database in config['databases']:
    if config['databases'][database]['NAME_JOIN']:
        config['databases'][database]['NAME'] = os.path.join(BASE_DIR, config['databases'][database]['NAME'])

DATABASES = config['databases']

# Logging
LOGGING = config['logging']
ADMINS = list(map(tuple, config['admins']))

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

DATETIME_FORMAT = 'l, F j, Y, g:i A O'

USE_I18N = True

USE_L10N = False

USE_TZ = True

if config['cache']['enabled']:
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': config['cache']['location']+config['cache']['port'],
        },
    }

    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_HOST = config['cache']['location']
    SESSION_REDIS_PORT = int(config['cache']['port'])
    SESSION_REDIS_DB = 0
    SESSION_REDIS_PREFIX = 'session'

if config['use_loadbalanced_databases']:
    DATABASE_ROUTERS = ('multidb.MasterSlaveRouter',)
    SLAVE_DATABASES = ['shadow-1']

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
TEMPLATES[0]['OPTIONS']['context_processors'].append("ctfapp.context_processors.site_configuration_processor")

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

CRISPY_TEMPLATE_PACK = "bootstrap3"

# Security stuff

CSRF_COOKIE_SECURE = config['ssl']
SESSION_COOKIE_SECURE = config['ssl']

CSRF_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = "DENY"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

if config['email']['enabled']:
    # SMTP info

    EMAIL_HOST = config['email']['host']
    EMAIL_HOST_USER = config['email']['username']
    EMAIL_HOST_PASSWORD = config['email']['password']
    if EMAIL_HOST_USER == "":
        EMAIL_HOST_USER = None
    if EMAIL_HOST_PASSWORD == "":
        EMAIL_HOST_PASSWORD = None
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    SERVER_EMAIL = 'angstromCTF Team <contact@angstromctf.com>'
    DEFAULT_FROM_EMAIL = 'angstromCTF Team <contact@angstromctf.com>'