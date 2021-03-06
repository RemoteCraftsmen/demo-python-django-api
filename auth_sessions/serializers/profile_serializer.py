"""
User profile serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    """
    Responses with Basic user profile data.
    """

    class Meta:
        """
        Meta Data - model and fields
        """

        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "date_joined",
        )
