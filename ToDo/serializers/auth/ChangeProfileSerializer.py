from rest_framework import serializers
from django.contrib.auth.models import User


class ChangeProfileSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'password_confirm']

        extra_kwargs = {
             'username': {'required': False}
        }

    def validate(self, attrs):
        user = self.instance
        errors = dict()

        if not user.check_password(attrs['password_confirm']):
            errors['password_confirm'] = list(["Wrong  password"])

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
