"""
Django settings for onit project.
Django 5.1.2
"""

import os
import dj_database_url
from sys import argv
from pathlib import Path

from libs.credentials_manager import get_secret


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Env - Production / development
if any(cmd in argv for cmd in ['runserver', 'shell', 'makemigrations', 'migrate']):
  ENV = "development"
else:
  ENV = "production"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("DJANGO_SECRET_KEY", ENV)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# List of domains that are allowed to make requests to this application
ALLOWED_HOSTS = [
    "api.onitafrica.com",
    "www.onitafrica.com",
    "onitafrica.com",
    "onit.production.up.railway.app",
    "localhost",
    "127.0.0.1",
    "0.0.0.0"
]

ADMIN = [("Neil", "neil@onitafrica.com")]

###############################################################################
#                            Application Defintion                            #
###############################################################################

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    'api',
    "django_extensions",
    "corsheaders",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "onit.urls"

# Web Server Gateway Interface (WSGI) application
WSGI_APPLICATION = "onit.wsgi.application"

###############################################################################
#                              API / Routing Settings                         #
###############################################################################

APPEND_SLASH = False
SECURE_SSL_REDIRECT = False

###############################################################################
#                               Cache Settings                                #
###############################################################################

CACHES = {
    "default": {
        "BACKEND": "services.cache.object_cache.ObjectCache"
    }
}

###############################################################################
#                              Database Settings                              #
###############################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_secret("DATABASE_NAME", ENV),
        "HOST": get_secret("DATABASE_ENDPOINT", ENV),
        'PORT': get_secret("DB_PORT", ENV),
        "USER": get_secret("DATABASE_USER", ENV),
        "PASSWORD": get_secret("DATABASE_PASSWORD", ENV)
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###############################################################################
#                        Password Validation Settings                         #
###############################################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    }
]

###############################################################################
#                        Internationalization Settings                        #
###############################################################################

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Johannesburg"
USE_I18N = True
USE_TZ = True

###############################################################################
#                            Static Files Settings                            #
###############################################################################

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

###############################################################################
#                               Content Sharing                               #
###############################################################################

# Content Origin Resource Sharing (CORS) settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://www.onitafrica.com',
    'http://www.onitafrica.com',
    "https://onit.production.up.railway.app",
    'http://localhost:3001',
    'http://localhost:8000'
]

CORS_ALLOW_CREDENTIALS = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cross-Site Request Forgery (CSRF) settings
CSRF_COOKIE_DOMAIN = '.onitafrica.com'
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True

CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = [
    'https://*.onitafrica.com',
    'https://*.railway.app',
    "https://onit.production.up.railway.app",
    'http://localhost:3001',
    'http://localhost:8000'
]

# Session settings
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = True

###############################################################################
#                             Debugging Settings                              #
###############################################################################

INTERNAL_IPS = [
    '127.0.0.1',
]
