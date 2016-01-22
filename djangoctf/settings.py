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
TEMPLATE_DEBUG = config['template_debug']
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

TEMPLATES = []

TEMPLATE_CONTEXT_PROCESSORS = ["django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages"]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

for database in config['databases']:
    if config['databases'][database]['NAME_JOIN']:
        config['databases'][database]['NAME'] = os.path.join(BASE_DIR, config['databases'][database]['NAME'])

DATABASES = config['databases']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

CRISPY_TEMPLATE_PACK = "bootstrap3"

# Security stuff

CSRF_COOKIE_SECURE = config['ssl']
SESSION_COOKIE_SECURE = config['ssl']

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = "DENY"
