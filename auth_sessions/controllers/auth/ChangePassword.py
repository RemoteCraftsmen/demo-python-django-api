from rest_framework import generics
from rest_framework.response import Response
from auth_sessions.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model


class ChangePassword(generics.CreateAPIView):
    """
    Change password for logged user
    * Requires password,newPassword, passwordConfirm  in body section
    """
    def post(self, request, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        serializer = ChangePasswordSerializer(data=request.data, context={
            'request': request,
            'user': user
        })
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response("Password has been changed")
