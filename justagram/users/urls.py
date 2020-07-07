from rest_framework.routers import SimpleRouter
from users.views import UserSignupViewSet, UserSignViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('signup', UserSignupViewSet)
router.register('', UserSignViewSet)
router.register('user', UserProfileViewSet)
urlpatterns = router.urls
