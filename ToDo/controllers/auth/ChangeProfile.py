from rest_framework import generics
from rest_framework.response import Response
from ToDo.serializers.auth import ChangeProfileSerializer
from django.contrib.auth.models import User


class ChangeProfile(generics.UpdateAPIView):
    """
    Change user data for logged user
    * Requires passwordConfirm  in body section
    """
    def put(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)

        serializer = ChangeProfileSerializer(instance=user, data=request.data,
                                             context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
