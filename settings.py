# Django settings for foia project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOCAL_DEVELOPMENT = False

import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'assets/')
MEDIA_URL = '/assets/'
# ADMIN_MEDIA_PREFIX = ''

SECRET_KEY = 'wcbp)q)=jz#-+wi3#a2v%w-9)e5jtbe+&ct8=@(3f%+!ud2gpw'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django_extensions',
    'foialist',
)

try:
    from settings_local import *
except ImportError:
    pass
