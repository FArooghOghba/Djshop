import os

from src.config.env import BASE_DIR, env


env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    'src.djshop.core.apps.CoreConfig',
    'src.djshop.common.apps.CommonConfig',
    'src.djshop.users.apps.UsersConfig',
    'src.djshop.catalog.apps.CatalogConfig',
    'src.djshop.authentication.apps.AuthenticationConfig',
    'src.djshop.media.apps.MediaConfig',
    'src.djshop.inventory.apps.InventoryConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'drf_spectacular',
    'django_extensions',
    'treebeard',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.config.urls'

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

WSGI_APPLICATION = 'src.config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': env('POSTGRES_ENGINE'),
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'users.BaseUser'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = '/vol/web/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/vol/web/media/'
MEDIA_URL = '/media/'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'src.djshop.api.exception_handlers.drf_default_with_modifications_exception_handler',
    # 'EXCEPTION_HANDLER': 'src.djshop.api.exception_handlers.hacksoft_proposed_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': []
}


# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env("REDIS_LOCATION", default="redis://localhost:6379"),
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from src.config.settings.celery import *  # noqa
from src.config.settings.cors import *  # noqa
from src.config.settings.jwt import *  # noqa
from src.config.settings.sessions import *  # noqa
from src.config.settings.swagger import *  # noqa


#from src.config.settings.sentry import * # noqa
#from src.config.settings.email_sending import * # noqa
