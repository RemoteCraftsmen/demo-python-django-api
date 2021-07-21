from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import logout


class Logout(generics.CreateAPIView):
    """
    Log out from system
    """
    def create(self, request, **kwargs):
        logout(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
