from django.urls import path
from django.conf.urls import include

from auth_sessions.routes import urlpatterns as auth_sessions_routes
from password_reset.routes.reset_password import urls as password_reset_routes

auth_urlpatterns = [
    path('auth/', include(auth_sessions_routes)),
    path('auth/', include(password_reset_routes)),
    path('auth/', include('rest_framework.urls')),
]