"""
Django settings for mainapp project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9lvu(w2w0udfw&bj%!j*%7q)1!-y2lzty2+nrbrb=#@g6hz^#a'
# django.setup()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'doc_filler_app',
    'clients',
    'psycopg2',
    'jsonfield',
    'login_auth',
    'django.forms',

    ##    'allauth.socialaccount',
    # 'django.contrib.sites.models',
    #    'json_field',
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates', '/login_auth/templates')],
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

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)

WSGI_APPLICATION = 'mainapp.wsgi.application'


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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

STATIC_DIR = os.path.join(BASE_DIR, 'static')
GENERETED_DOCS_DIR = os.path.join(STATIC_DIR, 'genereted_docs')
TEMPLATES_DIR = os.path.join(STATIC_DIR, 'template_docs')

STATICFILES_DIRS = [
    STATIC_DIR,						     #0
    GENERETED_DOCS_DIR,   	     #1
    os.path.join(GENERETED_DOCS_DIR, 'txt'),       #2
    os.path.join(GENERETED_DOCS_DIR, 'pdf'),	     #3
    os.path.join(GENERETED_DOCS_DIR, 'excel'),      #4
    os.path.join(GENERETED_DOCS_DIR, 'doc'),       #5
    TEMPLATES_DIR,    	  	 #6
    os.path.join(TEMPLATES_DIR, 'txt'),		 #7
    os.path.join(TEMPLATES_DIR, 'pdf'),		 #8
    os.path.join(TEMPLATES_DIR, 'excel'),	     #9
    os.path.join(TEMPLATES_DIR, 'doc'),		 #10
    os.path.join(TEMPLATES_DIR, 'css'),                       #11
    os.path.join(STATIC_DIR, 'js'),                        #12
    os.path.join(STATIC_DIR, 'img'),                       #13
]

TXT_TEMPL_DIR = STATICFILES_DIRS[7]
PDF_TEMPL_DIR = STATICFILES_DIRS[8]
EXEL_TEMPL_DIR = STATICFILES_DIRS[9]
DOC_TEMPL_DIR = STATICFILES_DIRS[10]

PDF_EXT = '.pdf'
DOC_EXT = '.doc'
DOCX_EXT = '.docx'
EXEL_EXT = '.xls'
TXT_EXT = '.txt'

PDF = 'pdf'
DOC = 'doc'
DOCX = 'docx'
EXEL = 'xls'
TXT = 'txt'

SITE_ID = 1

MEDIA_ROOT = os.path.join(BASE_DIR, 'media');
MEDIA_URL = '/media/';
