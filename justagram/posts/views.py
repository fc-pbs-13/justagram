from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(self.request)
        serializer.save(
            owner=self.request.user.profile
        )
