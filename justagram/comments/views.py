from time import sleep

from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.models import Post


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().prefetch_related('children')
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Comment.objects.all().select_related('post', 'user').prefetch_related('children')

        if self.action == 'list':
            qs = Comment.objects.all().prefetch_related('children')
            return qs

        return qs

    def perform_create(self, serializer):
        if 'comment_pk' in self.kwargs:
            parent = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
            serializer.save(user=self.request.user, parent=parent)
        else:
            post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
            serializer.save(user=self.request.user, post=post)

    # def retrieve(self, request, *args, **kwargs):
    #     key = f'comment_{kwargs["pk"]}'
    #     instance = cache.get(key)
    #     if not instance:
    #         instance = self.get_object()
    #         cache.set(key, instance, 3)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
