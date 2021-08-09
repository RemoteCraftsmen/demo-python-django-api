from .env import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
AUTH_USER_MODEL = 'users.User'
WSGI_APPLICATION = 'demo_python_django_api.wsgi.application'
