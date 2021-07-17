from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import logout
from ToDo.plugins.authentication.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class Logout(generics.CreateAPIView):
    """
    Log out from system
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def create(self, request, **kwargs):
        logout(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
