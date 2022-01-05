"""
Django settings for hmppctshmppc-backend project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

from celery.schedules import crontab


def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        raise ImproperlyConfigured(
            'Set the environment variable %s' % name
        )


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_var('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

PROJECT_APPS = [
    'core_api',
    'ekatagp'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hmppctshmppc_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'hmppctshmppc_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/public/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]

# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Cache

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://' + get_env_var('REDIS_HOST') + ':6379/1'
    }
}

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}

# Site type

SITE_TYPE = get_env_var('SITE_TYPE')

# Host URL

HOST_URL = get_env_var('HOST')

# Email Server Config

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_var('DJANGO_EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = get_env_var('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_var('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# CELERY

CELERY_BROKER_URL = 'redis://' + get_env_var('REDIS_HOST') + ':6379/0'
CELERY_RESULT_BACKEND = 'redis://' + get_env_var('REDIS_HOST') + ':6379/0'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'clean_access_token': {
        'task': 'core_api.tasks.task_clean_access_token',
        # NOTE: Need to check whether running at midnight is sufficient
        'schedule': crontab(minute=0, hour=0)
    },
    'clean_unused_payments': {
        'task': 'payment_processor.tasks.task_clean_unused_payments',
        'schedule': crontab(minute=0, hour=0)
    },
    'sync_currency_price': {
        'task': 'payment_processor.tasks.task_sync_currency_price',
        'schedule': crontab(minute='*/5')
    }
}

# Ekata GP
EKATA_GATEWAY_PROCESSOR_PROJECT_ID = get_env_var(
    'EKATA_GATEWAY_PROCESSOR_PROJECT_ID')
EKATA_GATEWAY_PROCESSOR_PROJECT_API_KEY = get_env_var(
    'EKATA_GATEWAY_PROCESSOR_PROJECT_API_KEY')
EKATA_GATEWAY_PROCESSOR_PAYMENT_SIGNATURE_SECRET = get_env_var(
    'EKATA_GATEWAY_PROCESSOR_PAYMENT_SIGNATURE_SECRET')
EKATA_GATEWAY_PROCESSOR_API_URL = get_env_var(
    'EKATA_GATEWAY_PROCESSOR_API_URL')
