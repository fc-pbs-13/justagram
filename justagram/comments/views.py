from rest_framework import viewsets, status
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.models import Post
from users.models import User


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        if request.data['parent']:
            parent_number = request.data['parent']
            parent = Comment.objects.get(id=int(parent_number))
            if not parent.parent:
                return super().create(request, *args, **kwargs)
        else:
            return super().create(request, *args, **kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(
            user=User.objects.get(id=self.kwargs['nested_1_pk']),
            post=Post.objects.get(id=self.kwargs['nested_2_pk']),
        )
