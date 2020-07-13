from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet

router = SimpleRouter(trailing_slash=False)
router.register('post', PostViewSet)

urlpatterns = router.urls
