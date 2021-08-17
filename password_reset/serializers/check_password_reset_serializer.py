from rest_framework import serializers


class CheckPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
