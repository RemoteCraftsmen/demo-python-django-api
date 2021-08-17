"""
Model User serializer.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Model User serializer. Provides basic user data and hyperlink to user details
    """
    class Meta:
        """
        Meta Data - model and fields
        """
        model = get_user_model()
        fields = ('url', 'email', 'is_staff', 'last_name', 'first_name', 'id')
