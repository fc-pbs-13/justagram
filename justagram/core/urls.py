from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, PhotoViewSet
from users.views import UserViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('post', PostViewSet)
router.register('photo', PhotoViewSet)
router.register('user', UserViewSet)
router.register('profile', UserProfileViewSet)

urlpatterns = router.urls
