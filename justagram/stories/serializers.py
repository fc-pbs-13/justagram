from rest_framework import serializers

from stories.models import Story, CheckShow
from users.serializers import UserSerializer


class StorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Story
        fields = (
            'id',
            'user',
            'time',
            'image',
        )


class CheckShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckShow
        fields = (
            'show_story',
            'show_user',
        )
