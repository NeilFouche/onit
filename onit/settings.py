"""
Django settings for onit project.
Django 5.1.2
"""

from pathlib import Path
from libs.credentials_manager import get_secret


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# List of domains that are allowed to make requests to this application
ALLOWED_HOSTS = [
    "onitweb.af-south-1.elasticbeanstalk.com",
    "client-side-rendering.d2aw166h87kmvv.amplifyapp.com"
    "api.onitafrica.com",
    "www.onitafrica.com",
    "13.247.63.128",  # Dedicated EC2 instance public IPv4 address
    "172.31.4.29",  # EC2 instance private IPv4 address
    "onitafrica.com",
    "localhost",
    "127.0.0.1",
    "0.0.0.0"
]

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
    'api',
    "django_extensions",
    "corsheaders",
]

MIDDLEWARE = [
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

ROOT_URLCONF = "onit.urls"

# Web Server Gateway Interface (WSGI) application
WSGI_APPLICATION = "onit.wsgi.application"

###############################################################################
#                              API / Routing Settings                         #
###############################################################################

APPEND_SLASH = False

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
        "ENGINE": "django.db.backends.mysql",
        "NAME": "onitdb",
        "HOST": "onit-db.c9ioyyeaczda.af-south-1.rds.amazonaws.com",
        'PORT': 3306,
        "USER": get_secret('DATABASE_USER'),
        "PASSWORD": get_secret("DATABASE_PASSWORD"),
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
    "http://onitweb.af-south-1.elasticbeanstalk.com",
    "https://client-side-rendering.d2aw166h87kmvv.amplifyapp.com",
    'https://www.onitafrica.com',
    'http://www.onitafrica.com',
    'http://localhost:3001',
    'http://localhost:8000'
]

CORS_ALLOW_CREDENTIALS = True

# Cross-Site Request Forgery (CSRF) settings
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [
    "http://onitweb.af-south-1.elasticbeanstalk.com",
    "https://api.onitafrica.com",
    "https://client-side-rendering.d2aw166h87kmvv.amplifyapp.com",
    'https://www.onitafrica.com',
    'http://www.onitafrica.com',
    'http://localhost:3001',
    'http://localhost'
]

SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True

###############################################################################
#                                Email Settings                               #
###############################################################################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.mail.us-east-1.awsapps.com"
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = "admin@onitafrica.com"
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = "admin@onitafrica.com"

###############################################################################
#                                Logging Settings                             #
###############################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

###############################################################################
#                             Debugging Settings                              #
###############################################################################

INTERNAL_IPS = [
    '127.0.0.1',
]
