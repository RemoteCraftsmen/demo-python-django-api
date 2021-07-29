from rest_framework import serializers
from django.contrib.auth import get_user_model


class ChangeProfileSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'last_name', 'first_name', 'password_confirm']


    def validate(self, attrs):
        user = self.instance
        errors = dict()

        if not user.check_password(attrs['password_confirm']):
            errors['password_confirm'] = list(["Wrong  password"])

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
