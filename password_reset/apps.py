"""
Configuration of password_reset App
"""
from django.apps import AppConfig


class PasswordResetConfig(AppConfig):
    """
    App config according to:
    https://docs.djangoproject.com/en/3.2/ref/applications/
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "password_reset"
