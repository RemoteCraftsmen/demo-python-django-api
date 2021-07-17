from rest_framework import routers
from ToDo.controllers import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urls = router.urls
