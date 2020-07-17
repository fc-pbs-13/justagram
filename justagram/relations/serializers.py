from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from relations.models import Follow


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = (
            'id',
            'from_follow_user',
            'to_follow_user',
        )

        read_only_fields = ('from_follow_user', 'to_follow_user')
    #
    # def validate(self, attrs):
    #     if Follow.objects.filter(from_follow_user=self.context['request'].user,
    #                              to_follow_user=self.context['view'].kwargs['profile_pk']).exists():
    #         raise serializers.ValidationError('The fields `from_user`, `to_user` must make a unique set.',
    #                                           code='unique')
    #
    #     return super().validate(attrs)
