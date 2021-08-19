"""
Routes for user profile
"""
from django.urls import path

from auth_sessions.views.profile.show import Show


urls = [
    path("profile", Show.as_view(), name="show_profile"),
]
