from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import logout
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView


class Logout(APIView):
    """
    Log out from system
    """
    @extend_schema(
        request=None,
        responses={
            401: OpenApiResponse(description='Unauthorized'),
        }, tags=["Auth"]
    )
    def post(self, request, **kwargs):
        logout(request)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
