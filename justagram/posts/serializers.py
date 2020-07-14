from rest_framework import serializers
from posts.models import Post, Photo


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
    name = serializers.CharField(source='owner.user.name', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'name',
            'contents',
            'photo',
            'input_photo',
        )

    def create(self, validated_data):
        images_data = validated_data.pop('input_photo')
        post = Post.objects.create(**validated_data)
        photo_bulk_list = []
        for image_data in images_data:
            photo = Photo(post=post, post_image=image_data)
            photo_bulk_list.append(photo)
        Photo.objects.bulk_create(photo_bulk_list)

        return post
