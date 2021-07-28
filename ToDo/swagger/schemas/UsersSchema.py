from drf_spectacular.utils import extend_schema
from ToDo.swagger.responses.forbidden import forbidden
from ToDo.swagger.responses.bad_request import bad_request
from ToDo.serializers import UserSerializer


class UsersSchema:
    list = extend_schema(description='Returns list of all users.', responses={200: UserSerializer, 403: forbidden},
                         tags=["Users"])
    retrieve = extend_schema(
        description='Returns details of user',
        responses={
            200: UserSerializer,
            403: forbidden
        },
        tags=["Users"])

    create = extend_schema(
        description='Creates new user.',
        responses={
            201: UserSerializer,
            400: bad_request,
            403: forbidden
        },
        tags=["Users"])

    destroy = extend_schema(
        description='Removes user.',
        responses={
            200: UserSerializer,
            403: forbidden
        },
        tags=["Users"])

    update = extend_schema(
        description='Updates user',
        responses={
            200: UserSerializer,
            400: bad_request,
            403: forbidden
        },
        tags=["Users"])
