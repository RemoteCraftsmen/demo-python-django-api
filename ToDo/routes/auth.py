
from ToDo.controllers.auth.Login import Login
from ToDo.controllers.auth.Logout import Logout
from django.urls import path


urls = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
]
