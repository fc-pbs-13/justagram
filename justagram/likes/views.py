from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from comments.models import Comment
from likes.models import CommentLike, PostLike
from likes.serializers import CommentLikeSerializer, PostLikeSerializer
from posts.models import Post


class CommentLikeViewSet(ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        to_like_comment = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
        serializer.save(
            from_like_comment=self.request.user,
            to_like_comment=to_like_comment,
        )


class PostLikeViewSet(ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        to_like_comment = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(
            from_like_post=self.request.user,
            to_like_post=to_like_comment,
        )
