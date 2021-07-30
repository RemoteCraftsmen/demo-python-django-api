from rest_framework import routers
from users.controllers.UserViewSet import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urls = router.urls
