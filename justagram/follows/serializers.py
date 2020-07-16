from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from follows.models import Follow


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'from_follow_user',
            'to_follow_user',
            'related_type'
        )

        read_only_fields = ('from_follow_user', 'to_follow_user')

    def validate(self, attrs):
        print(self.context['request'].user)
        print(self.context['view'].kwargs['profile_pk'])
        if Follow.objects.filter(from_follow_user=self.context['request'].user,
                                 to_follow_user=self.context['view'].kwargs['profile_pk']).exists():
            raise serializers.ValidationError('The fields `from_user`, `to_user` must make a unique set.',
                                              code='unique')

        return super().validate(attrs)
