"""
 Configuration of auth_session App
"""
from django.apps import AppConfig


class AuthUsersConfig(AppConfig):
    """
    App config according to:
    https://docs.djangoproject.com/en/3.2/ref/applications/
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_sessions"
