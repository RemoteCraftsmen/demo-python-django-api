from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth.models import User
from ToDo.serializers.auth.Register import RegisterSerializer
from ToDo.serializers.auth.Profile import ProfileSerializer
from django.contrib.auth import login
from ToDo.plugins.authentication.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class Register(views.APIView):
    """
    Register new user
    * Requires email, password, username, passwordConfirm  in body section
    """
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data['username']
        email = serializer.data['email']
        password = serializer.data['password']

        user = User.objects.create_user(username, email, password)
        login(request, user)

        return Response(ProfileSerializer(serializer.data).data)
