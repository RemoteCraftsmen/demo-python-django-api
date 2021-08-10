from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from password_reset.serializers.ResetPasswordSerializer import ResetPasswordSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from password_reset.swagger.responses.bad_request import bad_request


class RequestPasswordResetController(generics.CreateAPIView):
    """
    Reset Password
    * Requires email in body section
    """

    @extend_schema(
                   responses={
                       200: OpenApiResponse(description='OK', examples="Password has been changed"),
                       400: bad_request,
                   },
                   request=ResetPasswordSerializer,
                   tags=["Auth"])
    def post(self, request, **kwargs):
        password_reset_token = kwargs['token']
        user = get_user_model().objects.filter(passwordResetToken=password_reset_token).first()

        if user is None or user.is_password_reset_token_expired():
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ResetPasswordSerializer(data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)

        user.passwordResetTokenExpiresAt = None
        user.passwordResetToken = None
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response("Password has been changed", status=status.HTTP_200_OK)
