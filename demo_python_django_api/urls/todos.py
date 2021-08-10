from rest_framework import routers
from to_do.controllers import TodoViewSet

router_todos = routers.DefaultRouter()
router_todos.register(r'todos', TodoViewSet)
