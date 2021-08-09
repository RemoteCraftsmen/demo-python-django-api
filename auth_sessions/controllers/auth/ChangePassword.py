from rest_framework import generics
from rest_framework.response import Response
from auth_sessions.serializers import ChangePasswordSerializer
from django.contrib.auth import get_user_model
from auth_sessions.swagger.responses.bad_request import bad_request
from drf_spectacular.utils import extend_schema, OpenApiResponse


class ChangePassword(generics.CreateAPIView):
    """
    Change password for logged user
    * Requires password,newPassword, passwordConfirm  in body section
    """
    serializer_class = ChangePasswordSerializer

    @extend_schema(
                   responses={
                       200: ChangePasswordSerializer,
                       401: OpenApiResponse(description='Unauthorized'),
                       400: bad_request
                   },
                   request=ChangePasswordSerializer,
                   tags=["Auth"])
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
