"""
Django settings for demo_python_django_api project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from split_settings.tools import include

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

include(
    'mail.py',
    'database.py',
    'middleware.py',
    'apps.py',
    'rest_framework.py',
    'spectacular.py',
    'local.py',
    'password_validators.py',
    'templates.py',
    'allowed_hosts.py',
    'routing.py',
    'security.py',

)