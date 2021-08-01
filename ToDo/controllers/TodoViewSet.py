from rest_framework import viewsets, status
from ToDo.serializers.TodoSerializer import TodoSerializer
from ToDo.models import Todo
from auth_sessions.permissions.IsOwnerOrAdmin import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view
from ToDo.swagger.schemas.TodoSchema import TodoSchema
from ToDo.filters.TodoFilter import TodoFilter


@extend_schema_view(
    list=TodoSchema.list,
    retrieve=TodoSchema.retrieve,
    create=TodoSchema.create,
    destroy=TodoSchema.destroy,
    update=TodoSchema.update
)
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin, IsAuthenticated]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    filterset_class = TodoFilter

    def get_queryset(self):
        if self.request.user.is_staff:
            return Todo.objects.all()
        return Todo.objects.filter(owner=self.request.user.id)

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data, context={
            'request': request,
        })

        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
