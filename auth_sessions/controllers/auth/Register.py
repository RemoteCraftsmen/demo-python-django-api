from rest_framework import status, generics
from rest_framework.response import Response
from auth_sessions.serializers import RegisterSerializer, BasicUserSerializer
from django.contrib.auth import login
from operator import itemgetter
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse


class Register(generics.CreateAPIView):
    """
    Register new user
    * Requires email, password, username, passwordConfirm  in body section
    """
    @extend_schema(
            responses={
                200: BasicUserSerializer,
                401: OpenApiResponse(description='Unauthorized'),
            }, request=RegisterSerializer, tags=["Auth"])
    def post(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email, password = itemgetter('email', 'password')(serializer.validated_data)

        user = get_user_model().objects.create_user(email, password)
        login(request, user)

        return Response(BasicUserSerializer(serializer.data).data)
