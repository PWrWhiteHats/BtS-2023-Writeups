"""
Django settings for superficiality project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i4zynjn^)=^5j#1a@dm*q$=!mv(ouj-4$iij1+q#-r_ly$%8_8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    'superficiality-2-web.ch-dev.bts.wh.edu.pl',
    'superficiality-2-web.ch.bts.wh.edu.pl',
    'superficiality-2-web.ch1.bts.wh.edu.pl',
    'superficiality-2-web.ch2.bts.wh.edu.pl',
    'superficiality-2-web.ch3.bts.wh.edu.pl',
    'superficiality-2-web.ch4.bts.wh.edu.pl',
    'superficiality-2-web.ch5.bts.wh.edu.pl'
]


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',

    'django_extensions',

    'corsheaders',

    'main',
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',

    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',



    # 'main.middleware.handle_cors',
]

ROOT_URLCONF = 'superficiality.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'superficiality.wsgi.application'


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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] - %(message)s'
        }
    },

    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            'formatter': 'standard',
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },

    "loggers": {
        "root": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

WINNER_FLAG = "NOT AVAILABLE - CONTACT CTF ADMINISTRATOR"

try:
    with open("flag", "r") as flag_file:
        WINNER_FLAG = flag_file.read()
except FileNotFoundError:
    logger.error("THERE IS NO FLAG FILE IN THE WORKDIR")

try:
    from superficiality.local_settings import *
except ImportError:
    logger.warn("Local Settings not found")