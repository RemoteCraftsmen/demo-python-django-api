from rest_framework import status, generics
from rest_framework.response import Response
from ToDo.serializers.auth import RegisterSerializer, ProfileSerializer
from django.contrib.auth import login
from operator import itemgetter
from django.contrib.auth.models import User


class Register(generics.CreateAPIView):
    """
    Register new user
    * Requires email, password, username, passwordConfirm  in body section
    """

    def post(self, request, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        username, email, password = itemgetter('username', 'email', 'password')(serializer.validated_data)

        user = User.objects.create_user(username, email, password)
        login(request, user)

        return Response(ProfileSerializer(serializer.data).data)
