from rest_framework.serializers import ModelSerializer

from posts.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = {
            'owner',
            'post'
        }
        read_only_field = ['owner']
