"""demo_python_django_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from auth_sessions.plugins.error_handlers import no_found_error_handle
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework import routers
from ToDo.controllers import TodoViewSet
from users.controllers.UserViewSet import UserViewSet
from auth_sessions.routes import urlpatterns as auth_sessions_routes
from password_reset.routes.reset_password import urls as password_reset_routes


router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', include(router.urls)),
    path('api/', include(auth_sessions_routes)),
    path('api/', include(password_reset_routes)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

handler404 = no_found_error_handle
