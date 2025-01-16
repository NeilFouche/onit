"""
Django settings for onitweb project.
Django 5.1.2
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# List of domains that are allowed to make requests to this application
ALLOWED_HOSTS = ['www.onitafrica.com', 'localhost', '127.0.0.1']

###############################################################################
#                            Application Defintion                            #
###############################################################################

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "front",
    "django_extensions",
    "corsheaders",
    'rest_framework',
    'debug_toolbar',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
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

ROOT_URLCONF = "onitweb.urls"

# Web Server Gateway Interface (WSGI) application
WSGI_APPLICATION = "onitweb.wsgi.application"

###############################################################################
#                              API / Routing Settings                         #
###############################################################################

APPEND_SLASH = False

###############################################################################
#                               Cache Settings                                #
###############################################################################

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/{env('REDIS_DB')}"
    },
    "object_cache": {
        "BACKEND": "services.cache.object_cache.ObjectCache",
    }
}

###############################################################################
#                              Database Settings                              #
###############################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME"),
        "HOST": env("DATABASE_ENDPOINT"),
        'PORT': env('PORT'),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "ATOMIC_REQUESTS": False,
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

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

###############################################################################
#                               Content Sharing                               #
###############################################################################

# Content Origin Resource Sharing (CORS) settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001',
    'http://www.onitafrica.com',
    'http://localhost:8000'
]
CORS_ALLOW_CREDENTIALS = True

# Cross-Site Request Forgery (CSRF) settings
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3001',
    'http://www.onitafrica.com',
    'http://localhost'
]

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True

###############################################################################
#                                Email Settings                               #
###############################################################################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST_SERVER')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('EMAIL_DEFAULT_SENDER')

###############################################################################
#                             Debugging Settings                              #
###############################################################################

INTERNAL_IPS = [
    '127.0.0.1',
]
