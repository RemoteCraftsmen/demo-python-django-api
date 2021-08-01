from rest_framework import generics
from rest_framework.response import Response
from auth_sessions.serializers import ChangeProfileSerializer
from django.contrib.auth import get_user_model


class ChangeProfile(generics.UpdateAPIView):
    """
    Change user data for logged user
    * Requires passwordConfirm  in body section
    """
    def put(self, request, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)

        serializer = ChangeProfileSerializer(instance=user, data=request.data,
                                             context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
