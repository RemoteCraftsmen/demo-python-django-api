from rest_framework import routers
from users.controllers.UserViewSet import UserViewSet

router_users = routers.DefaultRouter()
router_users.register(r'users', UserViewSet)
