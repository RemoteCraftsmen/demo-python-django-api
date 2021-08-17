from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from password_reset.swagger.responses.bad_request import bad_request
from password_reset.serializers.check_password_reset_serializer import CheckPasswordResetSerializer
from password_reset.services.password_reset_token_generator_handler import PasswordResetTokenGeneratorHandler
from password_reset.services.date_service import DateService
from mail_templated import send_mail


class CheckPasswordResetController(generics.CreateAPIView):
    """
    Reset Password
    * Requires email in body section
    """
    serializer_class = CheckPasswordResetSerializer

    @extend_schema(
                   responses={
                       200: OpenApiResponse(description='OK'),
                       400: bad_request,
                   },
                   request=CheckPasswordResetSerializer,
                   tags=["Auth"])
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_model().objects.filter(email=serializer.validated_data['email']).first()

        if user is None:
            return Response("Check your mail")

        user.passwordResetToken = PasswordResetTokenGeneratorHandler.handle()
        user.passwordResetTokenExpiresAt = DateService.tomorrow()
        user.save()

        send_mail('email/password_reset.html', {'user': user, 'FRONTEND_URL': settings.FRONTEND_URL},
                  settings.DEFAULT_FROM_EMAIL, [user.email])

        return Response("Check your mail")
