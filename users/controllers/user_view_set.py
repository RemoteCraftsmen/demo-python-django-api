from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view

from users.swagger.schemas.users_schema import UsersSchema
from users.filters.user_filter import UserFilter

from users.serializers.user_serializer import UserSerializer


@extend_schema_view(
    list=UsersSchema.list,
    retrieve=UsersSchema.retrieve,
    create=UsersSchema.create,
    destroy=UsersSchema.destroy,
    update=UsersSchema.update)
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.filter(deleted__isnull=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    filterset_class = UserFilter
