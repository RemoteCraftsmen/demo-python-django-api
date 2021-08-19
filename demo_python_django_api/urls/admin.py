"""
Routes for admin endpoints
"""

from django.urls import path
from django.contrib import admin

admin_urlpatterns = [
    path("admin/", admin.site.urls),
]
