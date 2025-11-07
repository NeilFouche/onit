"""
WSGI config for onit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onit.settings")

import django
django.setup()

from django.contrib.auth.models import User
from django.db import connection

# Temporary database connection check
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("Database connection successful.")

    user_count = User.objects.count()
    print(f"User model is accessible. Total users: {user_count}")

except Exception as e:
    print(f"Database connection failed: {e}")

application = get_wsgi_application()
