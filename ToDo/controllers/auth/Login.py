from rest_framework import status, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from ToDo.serializers.auth import LoginSerializer, BasicUserSerializer
from django.contrib.auth import login
from operator import itemgetter
from drf_spectacular.utils import extend_schema, OpenApiResponse


class Login(generics.CreateAPIView):
    """
    Log into system
    * Requires email and password in body section
    """
    serializer_class = LoginSerializer

    @extend_schema(
                   responses={
                       200: BasicUserSerializer,
                       401: OpenApiResponse(description='Unauthorized'),
                   },
                   request=LoginSerializer,
                   tags=["Auth"])
    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email, password = itemgetter('email', 'password')(request.data)

        logged_user = User.objects.filter(email=email).first()

        if logged_user is None or not logged_user.check_password(password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if logged_user.check_password(password):
            login(request, logged_user)
            return Response(BasicUserSerializer(logged_user).data)
