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


class RetrieveSerializer(serializers.ModelSerializer):
    show = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = (
            'id',
            'user',
            'image',
            'show'
        )

    def get_show(self, obj):
        user = self.context.get('request')
        data = CheckShow.objects.filter(show_story=obj, show_user=user.user)
        return data.exists()


class CheckShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckShow
        fields = (
            'show_story',
            'show_user',
        )
