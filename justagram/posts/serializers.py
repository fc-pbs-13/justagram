from rest_framework import serializers
from posts.models import Post, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'post_image',
        )


class PostSerializer(serializers.ModelSerializer):
    photo = PhotoSerializer(many=True, read_only=True)
    name = serializers.CharField(source='owner.user.name', read_only=True)

    class Meta:
        model = Post
        fields = (
            'name',
            'contents',
            'photo',
        )

