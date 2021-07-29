from rest_framework import serializers
from django.contrib.auth import get_user_model


class Profile(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')
