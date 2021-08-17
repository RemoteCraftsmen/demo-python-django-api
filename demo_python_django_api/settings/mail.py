"""
Settings for connection with mail server
"""
from distutils.util import strtobool
from .env import env

EMAIL_HOST = env("EMAIL_HOST") or "127.0.0.1"
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL") or "Test User <user@example.com>"
EMAIL_HOST_USER = env("EMAIL_HOST_USER") or ""
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD") or ""
EMAIL_PORT = env("EMAIL_PORT") or 1025
EMAIL_USE_TLS = bool(strtobool(env("EMAIL_USE_TLS"))) or False
