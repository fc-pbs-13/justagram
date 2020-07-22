from rest_framework import serializers

from comments.models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'comment',
            'parent',
            'post',
            'user',
            'children',
            'like_count',
        )
        read_only_fields = ['user', 'post', 'like_count']
