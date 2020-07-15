from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from comments.views import CommentViewSet
from posts.views import PostViewSet, PhotoViewSet
from users.views import UserViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('post', PostViewSet)
router.register('photo', PhotoViewSet)
router.register('user', UserViewSet)
router.register('profile', UserProfileViewSet)
router.register('comment', CommentViewSet)

user_router = routers.NestedSimpleRouter(router, 'user')
user_router.register('post', PostViewSet)
user_router.register('profile', UserProfileViewSet)

post_router = routers.NestedSimpleRouter(user_router, 'post')
post_router.register('photo', PhotoViewSet)
post_router.register('comment', CommentViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(user_router.urls)),
    url('', include(post_router.urls)),
]
