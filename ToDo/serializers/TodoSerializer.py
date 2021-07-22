from rest_framework import serializers
from ToDo.models import Todo
from ToDo.serializers.UserSerializer import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Todo
        fields = ('url', 'id', 'name', 'completed', 'owner')

    def create(self, validated_data):
        todo = Todo.objects.create(owner=self.context['request'].user, name=validated_data['name'],
                                   completed=validated_data['completed'])
        return todo
