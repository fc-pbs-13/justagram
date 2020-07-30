from rest_framework import serializers
from tags.models import Tag, TagPost


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'tag_name',
            'count_tag',
        )

        read_only_fields = ('count_tag', 'tag_name')


class TagShowSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = TagPost
        fields = (
            'tag',
        )


class TagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = (
            'id',
            'post',
            'tag'
        )
