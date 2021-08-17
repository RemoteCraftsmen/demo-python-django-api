"""
Allowed host settings
"""
from .env import env

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',') or ['127.0.0.1']
