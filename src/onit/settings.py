"""
Django settings for onit project.
Django 5.1.2
"""

from decouple import config
from django.core.management.utils import get_random_secret_key
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DJANGO_DEBUG", cast=bool, default=True)

# Application environment
ENV = config("ENVIRONMENT", cast=str, default="development")
print(f"Running in {ENV} environment")

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

if DEBUG:
    ALLOWED_HOSTS = ["*"]

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
        "NAME": config("DATABASE_NAME", "postgres"),
        "HOST": config("DATABASE_ENDPOINT", default="127.0.0.1"),
        'PORT': config("DB_PORT", default=5432, cast=int),
        "USER": config("DATABASE_USER", default="postgres"),
        "PASSWORD": config("DATABASE_PASSWORD", default="develop")
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
