from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from likes.models import PostLike, CommentLike


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'id',
            'from_like_post',
            'to_like_post'
        )
        read_only_fields = ('from_like_post', 'to_like_post')

    def validate(self, attrs):
        print(1)
        if PostLike.objects.filter(from_like_post=self.context['request'].user,
                                   to_like_post=self.context['view'].kwargs['post_pk']).exists():
            raise serializers.ValidationError('The fields `from_user`, `to_user` must make a unique set.',
                                              code='unique')

        return super().validate(attrs)


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = CommentLike
        fields = (
            'id',
            'from_like_comment',
            'to_like_comment'
        )
        read_only_fields = ('from_like_comment', 'to_like_comment')

    def validate(self, attrs):
        if CommentLike.objects.filter(from_like_comment=self.context['request'].user,
                                      to_like_comment=self.context['view'].kwargs['comment_pk']).exists():
            raise serializers.ValidationError('The fields `from_user`, `to_user` must make a unique set.',
                                              code='unique')

        return super().validate(attrs)
