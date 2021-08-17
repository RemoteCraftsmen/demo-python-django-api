"""
Django Admin Panel configuration
https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
"""
from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted

from to_do.models import Todo


class SafeDeleteAdminView(SafeDeleteAdmin):
    """
    Settings for models that inherent from Safe Delete model
    """

    list_display = (
        highlight_deleted,
        "name",
        "completed",
        "owner",
    ) + SafeDeleteAdmin.list_display
    list_filter = ("completed",) + SafeDeleteAdmin.list_filter


admin.site.register(Todo, SafeDeleteAdminView)
