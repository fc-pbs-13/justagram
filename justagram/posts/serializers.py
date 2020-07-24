from rest_framework import serializers

from comments.serializers import CommentSerializer
from posts.models import Post, Photo
from tags.models import Tag, TagPost


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'post',
            'post_image',
        )
        read_only_fields = ['post']


class PostSerializer(serializers.ModelSerializer):
    input_photo = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
    )
    photo = PhotoSerializer(many=True, read_only=True)
    name = serializers.CharField(source='owner.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tag = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'contents',
            'photo',
            'input_photo',
            'comments',
            'like_count',
            'tag'
        )
        read_only_fields = ('like_count', 'tag')

    def create(self, validated_data):
        images_data = validated_data.pop('input_photo')
        tag_data = validated_data.pop('tag')

        post = Post.objects.create(**validated_data)

        photo_bulk_list = []

        for image_data in images_data:
            photo = Photo(post=post, post_image=image_data)
            photo_bulk_list.append(photo)
        Photo.objects.bulk_create(photo_bulk_list)

        for tag in tag_data:
            tag, _ = Tag.objects.get_or_create(tag_name=tag)
            TagPost.objects.create(
                post=post,
                tag=tag
            )

        return post
