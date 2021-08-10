from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from auth_sessions.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from auth_sessions.swagger.responses.bad_request import bad_request


class Show(generics.RetrieveAPIView):
    """
    Shows logged user data(profile).
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            responses={
                200: ProfileSerializer,
                401: OpenApiResponse(description='Unauthorized'),
                400: bad_request
            }, request=ProfileSerializer, tags=["Auth"])
    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        user = get_user_model().objects.get(id=logged_user_id)
        serializer = self.serializer_class(user)

        return Response(serializer.data)
