from rest_framework import viewsets,status
from ToDo.serializers.TodoSerializer import TodoSerializer
from ToDo.models import ToDo
from ToDo.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TodoViewSet(viewsets.ModelViewSet):
    """
    Returns List of all users
    TODO Remove or split this to separate  dirs and files;
    """
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    queryset = ToDo.objects.all()
    serializer_class = TodoSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return ToDo.objects.all()
        return ToDo.objects.filter(owner=self.request.user.id)


    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
        })

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)
