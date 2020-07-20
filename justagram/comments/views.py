from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.models import Post


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if 'comment_pk' in self.kwargs:
            parent = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
            serializer.save(user=self.request.user, parent=parent)
        else:
            post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
            serializer.save(user=self.request.user, post=post)
