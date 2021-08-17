"""
Register View
"""
from operator import itemgetter

from django.contrib.auth import login
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from auth_sessions.swagger.responses.bad_request import bad_request
from auth_sessions.serializers import RegisterSerializer, BasicUserSerializer


class Register(generics.CreateAPIView):
    """
    Register new user
    * Requires email, password, username, passwordConfirm  in body section
    """
    serializer_class = RegisterSerializer

    @extend_schema(
            responses={
                200: BasicUserSerializer,
                401: OpenApiResponse(description='Unauthorized'),
                400: bad_request
            }, request=RegisterSerializer, tags=["Auth"])
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        email, password = itemgetter('email', 'password')(serializer.validated_data)

        user = get_user_model().objects.create_user(email, password)
        login(request, user)

        return Response(BasicUserSerializer(serializer.data).data)
