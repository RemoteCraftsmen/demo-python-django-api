"""
Filters for user model.
"""
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


class UserFilter(filters.FilterSet):
    """
    Filter set for user model. Allows to filter by first and last name, email, is_staff,is_active, string contains
    """

    first_name_like = filters.CharFilter(
        field_name="first_name", lookup_expr="contains"
    )
    last_name_like = filters.CharFilter(field_name="last_name", lookup_expr="contains")
    email_like = filters.CharFilter(field_name="email", lookup_expr="contains")

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "is_staff", "is_active")
