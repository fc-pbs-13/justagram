from rest_framework import serializers

from posts.models import Post
from tags.models import Tag, TagPost


class TagSerializer(serializers.ModelSerializer):
    tag_data = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True
    )

    class Meta:
        model = Tag
        fields = (
            'id',
            'tag_name',
            'tag_data',
            'count_tag',
        )

        read_only_fields = ('count_tag', 'tag_name')


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = (
            'id',
            'post',
            'tag'
        )
