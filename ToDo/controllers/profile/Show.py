from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from ToDo.serializers.auth import Profile
from rest_framework.permissions import IsAuthenticated


class Show(generics.RetrieveAPIView):
    """
    Shows logged user data(profile).
    """
    serializer_class = Profile
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        user = User.objects.get(id=logged_user_id)
        serializer = self.serializer_class(user)

        return Response(serializer.data)
