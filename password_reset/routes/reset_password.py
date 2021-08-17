from password_reset.controllers.check_password_reset_controller import CheckPasswordResetController
from password_reset.controllers.request_password_reset_controller import RequestPasswordResetController

from django.urls import path

urls = [
    path('password-reset/<str:token>', RequestPasswordResetController.as_view(), name='password_reset_token'),
    path('password-reset', CheckPasswordResetController.as_view(), name='password_reset'),
]
