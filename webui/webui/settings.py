"""
Django settings for webui project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from dotenv import load_dotenv
from pathlib import Path
from os import getenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# DEBUG parents vs parent
BASE_DIR = Path(__file__).resolve().parents[1]
WEBENV = Path(__file__).resolve().parents[2] / 'webenv'

load_dotenv(WEBENV)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from django.core.management.utils import get_random_secret_key
SECRET_KEY = getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
IS_DEVELOPMENT = getenv('IS_DEVELOPMENT', 'True').casefold()
if IS_DEVELOPMENT == 'false':
    IS_DEVELOPMENT = False
elif IS_DEVELOPMENT == 'true':
    IS_DEVELOPMENT = True
DEBUG = IS_DEVELOPMENT

ALLOWED_HOSTS = [host.strip() for host in getenv('ALLOWED_HOSTS', "*").split(',')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'controls',
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

ROOT_URLCONF = 'webui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'webui.wsgi.application'
ASGI_APPLICATION = 'webui.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # where all static files are served from
# MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# auth
LOGIN_REDIRECT_URL = 'dashboard-page'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# message stuff
from django.contrib.messages import constants as messages

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# This sets the mapping of message level to message tag, which is typically rendered as a CSS class in HTML
MESSAGE_TAGS = {
    messages.ERROR: 'error',
    messages.SUCCESS: 'success',
    messages.INFO: 'info',
    messages.WARNING: 'warning',
    messages.DEBUG: 'debug',
}