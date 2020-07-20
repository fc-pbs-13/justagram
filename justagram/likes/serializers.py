from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from likes.models import PostLike, CommentLike


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'id',
            'post_user',
            'to_like_post'
        )
        read_only_fields = ('post_user', 'to_like_post')

    def validate(self, data):
        if PostLike.objects.filter(post_user=self.context['request'].user,
                                   to_like_post=self.context['view'].kwargs['post_pk']).exists():
            raise serializers.ValidationError('The fields `from_user`, `to_user` must make a unique set.',
                                              code='unique')

        return data


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = (
            'id',
            'comment_user',
            'to_like_comment'
        )
        read_only_fields = ('comment_user', 'to_like_comment')
