"""
Basic User serializer
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model


class BasicUserSerializer(serializers.ModelSerializer):
    """
    Returns basic user data
    """

    class Meta:
        """
        Meta Data - model and fields
        """

        model = get_user_model()
        fields = ("email", "first_name", "last_name")
