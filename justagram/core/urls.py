from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from comments.views import CommentViewSet
from follows.views import FollowViewSet
from likes.views import CommentLikeViewSet, PostLikeViewSet
from posts.views import PostViewSet, PhotoViewSet
from users.views import UserViewSet, UserProfileViewSet

router = SimpleRouter(trailing_slash=False)
router.register('post', PostViewSet)
router.register('photo', PhotoViewSet)
router.register('user', UserViewSet)
router.register('profile', UserProfileViewSet)
router.register('comment', CommentViewSet)
router.register('follow', FollowViewSet)
router.register('post_like', PostLikeViewSet)
router.register('comment_like', CommentLikeViewSet)

user_router = routers.NestedSimpleRouter(router, 'user')
user_router.register('post', PostViewSet)
user_router.register('profile', UserProfileViewSet)

profile_router = routers.NestedSimpleRouter(router, 'profile', lookup='profile')
profile_router.register('follow', FollowViewSet)

comment_router = routers.NestedSimpleRouter(router, 'comment', lookup='comment')
comment_router.register('comment', CommentViewSet)
comment_router.register('comment_like', CommentLikeViewSet)

post_like_router = routers.NestedSimpleRouter(router, 'post', lookup='post')
post_like_router.register('post_like', PostLikeViewSet)

post_router = routers.NestedSimpleRouter(user_router, 'post', lookup='post')
post_router.register('photo', PhotoViewSet)
post_router.register('comment', CommentViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(user_router.urls)),
    url('', include(post_router.urls)),
    url('', include(comment_router.urls)),
    url('', include(profile_router.urls)),
    url('', include(post_like_router.urls)),
]
