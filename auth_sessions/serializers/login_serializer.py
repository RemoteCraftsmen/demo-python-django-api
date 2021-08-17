"""
Seralizer for logging user
"""
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Request Login serializer, write only
    """
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
