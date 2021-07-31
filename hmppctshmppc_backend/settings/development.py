from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

# CORS
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000'
]

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'access-token'
)
