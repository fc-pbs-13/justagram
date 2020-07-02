from rest_framework.routers import SimpleRouter

from users.views import UserInfoViewSet, UserProfile

router = SimpleRouter(trailing_slash=False)
router.register('resister', UserInfoViewSet)
router.register('user', UserProfile)
urlpatterns = router.urls
