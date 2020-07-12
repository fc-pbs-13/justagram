from rest_framework.serializers import ModelSerializer

from posts.models import Post, Photo


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'owner',
            'contents',
        )
        read_only_fields = ('owner',)


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'post_image',
        )
