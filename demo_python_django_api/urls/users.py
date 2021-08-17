"""
Routes for endpoints that correspond with user model
"""
from rest_framework import routers
from users.views.user_view_set import UserViewSet

router_users = routers.DefaultRouter()
router_users.register(r"users", UserViewSet)
