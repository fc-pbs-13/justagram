from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Photo
from posts.serializers import PostSerializer, PhotoSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('owner') \
        .prefetch_related('photo', 'post_comments__children', 'tags__tag',)
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
