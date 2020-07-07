from rest_framework.routers import SimpleRouter
from users.views import UserViewSet, UserSignViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('signup', UserViewSet)
router.register('', UserSignViewSet)
router.register('user', UserProfileViewSet)
urlpatterns = router.urls
