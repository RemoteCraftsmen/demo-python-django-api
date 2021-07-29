from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


class UserFilter(filters.FilterSet):
    username_like = filters.CharFilter(field_name='username', lookup_expr='contains')
    first_name_like = filters.CharFilter(field_name='first_name', lookup_expr='contains')
    last_name_like = filters.CharFilter(field_name='last_name', lookup_expr='contains')
    email_like = filters.CharFilter(field_name='email', lookup_expr='contains')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
