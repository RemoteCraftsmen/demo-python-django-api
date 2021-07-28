from django_filters import rest_framework as filters
from ToDo.models import Todo


class TodoFilter(filters.FilterSet):
    name_like = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Todo
        fields = ('name', 'completed', 'owner')
