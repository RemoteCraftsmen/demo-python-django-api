
from auth_sessions.controllers.auth.Login import Login
from auth_sessions.controllers.auth.Logout import Logout
from auth_sessions.controllers.auth.Register import Register
from auth_sessions.controllers.auth.ChangePassword import ChangePassword
from auth_sessions.controllers.auth.ChangeProfile import ChangeProfile

from django.urls import path


urls = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('register', Register.as_view(), name='register'),
    path('change-password', ChangePassword.as_view(), name='change_password'),
    path('change-profile', ChangeProfile.as_view(), name='change_profile'),
]
