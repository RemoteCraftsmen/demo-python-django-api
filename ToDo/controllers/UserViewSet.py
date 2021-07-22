from rest_framework import viewsets, permissions
from ToDo.serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    Returns List of all users
    TODO Remove or split this to separate  dirs and files; add only for admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
