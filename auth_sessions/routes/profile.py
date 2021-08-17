from django.urls import path

from auth_sessions.controllers.profile.Show import Show


urls = [
    path('profile', Show.as_view(), name='show_profile'),
]
