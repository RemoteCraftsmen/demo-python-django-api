from auth_sessions.controllers.profile.Show import Show
from django.urls import path


urls = [
    path('profile', Show.as_view(), name='show_profile'),
]
