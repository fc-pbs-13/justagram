from rest_framework.routers import SimpleRouter
from users.views import UserViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('user', UserViewSet)
router.register('profile', UserProfileViewSet)
urlpatterns = router.urls
