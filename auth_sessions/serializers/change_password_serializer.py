"""
Change Password Serializer
"""

from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class ChangePasswordSerializer(serializers.Serializer):
    """
    Request serializer for change password.
    """

    password = serializers.CharField(
        min_length=8,
        required=True,
    )
    password_confirm = serializers.CharField(
        min_length=8,
        required=True,
    )
    old_password = serializers.CharField(
        min_length=8,
        required=True,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        user = self.instance
        errors = dict()

        try:
            validators.validate_password(password=attrs["password"], user=user)
        except exceptions.ValidationError as error:
            errors["password"] = list(error.messages)

        if not user.check_password(attrs["old_password"]):
            errors["old_password"] = list(["Wrong old password"])

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
