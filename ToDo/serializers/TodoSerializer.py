from rest_framework import serializers
from ToDo.models import Todo
from ToDo.serializers.UserSerializer import UserSerializer
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    owner_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Todo
        fields = ('url', 'id', 'name', 'completed', 'owner', 'owner_id')

    def create(self, validated_data):
        if self.context['request'].user.is_staff and validated_data['owner_id'] is not None:
            owner = User.objects.filter(id=validated_data['owner_id']).first()
        else:
            owner = self.context['request'].user

        todo = Todo.objects.create(owner=owner, name=validated_data['name'],
                                   completed=validated_data['completed'])
        return todo

    def update(self, instance, validated_data):
        if self.context['request'].user.is_staff and validated_data['owner_id'] is not None:
            owner = User.objects.filter(id=validated_data['owner_id']).first()
        else:
            owner = self.context['request'].user

        todo = instance
        todo.name = validated_data['name']
        todo.completed = validated_data['completed']
        todo.owner = owner
        todo.save()

        return todo
