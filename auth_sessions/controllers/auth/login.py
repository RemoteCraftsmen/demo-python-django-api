"""
Logging in view
"""
from operator import itemgetter

from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema, OpenApiResponse

from auth_sessions.swagger.responses.bad_request import bad_request
from auth_sessions.serializers import LoginSerializer, BasicUserSerializer


class Login(generics.CreateAPIView):
    """
    Log into system
    * Requires email and password in body section
    """

    serializer_class = LoginSerializer

    @extend_schema(
        responses={
            200: BasicUserSerializer,
            401: OpenApiResponse(description="Unauthorized"),
            400: bad_request,
        },
        request=LoginSerializer,
        tags=["Auth"],
    )
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        email, password = itemgetter("email", "password")(request.data)
        logged_user = get_user_model().objects.filter(email=email).first()

        if logged_user is None or not logged_user.check_password(password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if logged_user.check_password(password):
            login(request, logged_user)

            return Response(BasicUserSerializer(logged_user).data)
