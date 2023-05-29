import os
from .base import *
import environ


DEBUG = False

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': env('SQL_ENGINE', default='django.db.backends.sqlite3'),
#         'NAME': env('SQL_DATABASE', default=os.path.join(BASE_DIR, 'db.sqlite3')),
#         'USER': env('SQL_USER', default='user'),
#         'PASSWORD': env('SQL_PASSWORD', default='password'),
#         'HOST': env('SQL_HOST', default='localhost'),
#         'PORT': env('SQL_PORT', default=''),
#     }
# }

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True