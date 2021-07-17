from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from ToDo.serializers.auth.Login import LoginSerializer
from ToDo.serializers.auth.Profile import ProfileSerializer
from django.contrib.auth import login
from ToDo.plugins.authentication.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class Login(views.APIView):
    """
    Log into system
    * Requires email and password in body section
    """
    serializer_class = LoginSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        password = request.data['password']
        logged_user = User.objects.filter(email=email).first()

        if logged_user is None or not logged_user.check_password(password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if logged_user.check_password(password):
            login(request, logged_user)
            return Response(ProfileSerializer(logged_user).data)
