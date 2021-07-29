from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    username = serializers.CharField(min_length=8, required=True,
                                     validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True,)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_confirm', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        user = get_user_model()(attrs['username'], attrs['email'], attrs['password'])
        errors = dict()

        try:
            validators.validate_password(password=attrs['password'], user=user)
        except exceptions.ValidationError as error:
            errors['password'] = list(error.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
