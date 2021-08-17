"""
To_do Serializer
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from to_do.models import Todo
from users.serializers.user_serializer import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    """
    Standart request/response serializer for to_do model
    """
    owner = UserSerializer(many=False, read_only=True)
    owner_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        """
        Meta Data - model and fields
        """
        model = Todo
        fields = ('url', 'id', 'name', 'completed', 'owner', 'owner_id')

    def create(self, validated_data):
        if self.context['request'].user.is_staff and validated_data['owner_id'] is not None:
            owner = get_user_model().objects.filter(id=validated_data['owner_id']).first()
        else:
            owner = self.context['request'].user

        todo = Todo.objects.create(owner=owner, name=validated_data['name'],
                                   completed=validated_data['completed'])
        return todo

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff and validated_data['owner_id'] is not None:
            owner = get_user_model().objects.filter(id=validated_data['owner_id']).first()
        else:
            owner = self.context['request'].user

        todo = instance
        todo.name = validated_data['name']
        todo.completed = validated_data['completed']
        todo.owner = owner
        todo.save()

        return todo
