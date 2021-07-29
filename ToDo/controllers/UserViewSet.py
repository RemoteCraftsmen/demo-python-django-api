from rest_framework import viewsets, permissions
from ToDo.serializers import UserSerializer
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from ToDo.swagger.schemas.UsersSchema import UsersSchema
from ToDo.filters.UserFilter import UserFilter


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
