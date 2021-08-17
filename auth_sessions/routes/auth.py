"""
Routes for auth_session
"""
from django.urls import path

from auth_sessions.controllers.auth.login import Login
from auth_sessions.controllers.auth.logout import Logout
from auth_sessions.controllers.auth.register import Register
from auth_sessions.controllers.auth.change_password import ChangePassword
from auth_sessions.controllers.auth.change_profile import ChangeProfile


urls = [
    path("login", Login.as_view(), name="login"),
    path("logout", Logout.as_view(), name="logout"),
    path("register", Register.as_view(), name="register"),
    path("change-password", ChangePassword.as_view(), name="change_password"),
    path("change-profile", ChangeProfile.as_view(), name="change_profile"),
]
