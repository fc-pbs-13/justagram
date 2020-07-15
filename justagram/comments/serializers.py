from rest_framework import serializers

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id',
            'comment',
            'parent',
            'post',
            'user',
        )
        read_only_fields = ['user', 'post']
