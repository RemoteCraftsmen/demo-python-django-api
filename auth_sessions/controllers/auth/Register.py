from rest_framework import status, generics
from rest_framework.response import Response
from auth_sessions.serializers import RegisterSerializer, BasicUserSerializer
from django.contrib.auth import login
from operator import itemgetter
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from auth_sessions.swagger.responses.bad_request import bad_request


class Register(generics.CreateAPIView):
    """
    Register new user
    * Requires email, password, username, passwordConfirm  in body section
    """
    @extend_schema(
            responses={
                200: BasicUserSerializer,
                401: OpenApiResponse(description='Unauthorized'),
                400: bad_request
            }, request=RegisterSerializer, tags=["Auth"])
    def post(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        email, password = itemgetter('email', 'password')(serializer.validated_data)

        user = get_user_model().objects.create_user(email, password)
        login(request, user)

        return Response(BasicUserSerializer(serializer.data).data)
