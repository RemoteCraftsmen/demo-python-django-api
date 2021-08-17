"""
Settings for all routes in system
"""
from django.urls import path
from django.conf.urls import include
from auth_sessions.plugins.error_handlers import no_found_error_handle

from .auth import auth_urlpatterns
from .spectacular import swagger_urlpatterns
from .admin import admin_urlpatterns
from .todos import router_todos
from .users import router_users


urlpatterns = [
    path('', include(admin_urlpatterns)),
    path('', include(swagger_urlpatterns)),
    path('api/', include(router_users.urls)),
    path('api/', include(router_todos.urls)),
    path('api/', include(auth_urlpatterns)),
]

handler404 = no_found_error_handle
