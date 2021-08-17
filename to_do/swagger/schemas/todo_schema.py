from drf_spectacular.utils import extend_schema
from to_do.swagger.responses.forbidden import forbidden
from to_do.swagger.responses.bad_request import bad_request
from to_do.serializers.todo_serializer import TodoSerializer


class TodoSchema:
    list = extend_schema(
        description="Returns list of all Todos that belong to user; list of all Todos if logged as admin.",
        responses={200: TodoSerializer, 403: forbidden},
        tags=["Todos"],
    )
    retrieve = extend_schema(
        description="Returns details of Todo item. ",
        responses={200: TodoSerializer, 403: forbidden},
        tags=["Todos"],
    )
    create = extend_schema(
        description="Creates new Todo item",
        responses={201: TodoSerializer, 400: bad_request, 403: forbidden},
        tags=["Todos"],
    )
    destroy = extend_schema(
        description="Removes Todo item",
        responses={200: TodoSerializer, 403: forbidden},
        tags=["Todos"],
    )
    update = extend_schema(
        description="Updates Todo item",
        responses={200: TodoSerializer, 400: bad_request, 403: forbidden},
        tags=["Todos"],
    )
