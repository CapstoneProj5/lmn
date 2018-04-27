"""
Django settings for LMNOPsite project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8c01$#j44g3znb)$q0()8)!%ts-jc)k12!a75-!63qb%bj=d4k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lmn'
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


ROOT_URLCONF = 'lmnop_project.urls'

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
                'django.template.context_processors.media',  # to access the media url
            ],
        },
    },
]

WSGI_APPLICATION = 'lmnop_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lmnop',
        'USER': 'lmnop',
        'PASSWORD': os.environ['LMNOP_DB_PW'],
        'HOST': '/cloudsql/lmnop-2905:us-central1:lmnop',
        'PORT': '5432',

        # This ties HTTP request/response to db transactions by default
        # Otherwise, Django will easily permit partly-completed db updates
        'ATOMIC_REQUESTS': True,

        # Postgres works best this way, and applications usually assume this implicitly
        'isolation_level': "serializable",
        'TEST': {'CREATE_DB': False} 

    }
}

if not os.getenv('GAE_INSTANCE'):
    DATABASES['default']['HOST'] = '127.0.0.1'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Google Cloud Storage API creds
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'lmnop-2905'
GS_STATIC_APP_FILES_BUCKET = 'lmnop-2905.appspot.com'
STATIC_URL = 'https://storage.googleapis.com/%s/static/' % GS_STATIC_APP_FILES_BUCKET
MEDIA_URL = 'https://storage.googleapis.com/%s/media/' % GS_BUCKET_NAME

# Where to send user after successful login if no other page is provided.
# Should provide the user object.
LOGIN_REDIRECT_URL = 'lmn:my_user_profile'
LOGOUT_REDIRECT_URL = 'lmn:logged_out'

django_heroku.settings(locals())
