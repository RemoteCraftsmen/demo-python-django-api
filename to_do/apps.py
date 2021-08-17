"""
Configuration of to_do App
"""
from django.apps import AppConfig


class TodoConfig(AppConfig):
    """
    App config according to:
    https://docs.djangoproject.com/en/3.2/ref/applications/
    """

    default_auto_field = "django.db.models.AutoField"
    name = "to_do"
