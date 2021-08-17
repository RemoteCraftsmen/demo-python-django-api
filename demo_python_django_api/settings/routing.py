"""
Routing settings
"""

from .env import env

ROOT_URLCONF = 'demo_python_django_api.urls'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

APPEND_SLASH = False
FRONTEND_URL = env('FRONTEND_URL') or '127.0.0.1:8000/'
