from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Photo
from posts.serializers import PostSerializer, PhotoSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
