from rest_framework import serializers
from ToDo.models import ToDo
from ToDo.serializers.UserSerializer import UserSerializer


class TodoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = ToDo
        fields = ('url', 'id', 'name', 'completed', 'owner')

    def create(self, validated_data):
        todo = ToDo.objects.create(owner=self.context['request'].user, name=validated_data['name'],
                                   completed=validated_data['completed'])
        return todo
