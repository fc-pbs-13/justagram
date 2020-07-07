from rest_framework import serializers

from users.models import User, UserProfile
from rest_framework.serializers import ModelSerializer


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'nickname',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserSignSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

        extra_kwargs = {
            'email': {'write_only': True},
            'password': {'write_only': True},
        }


class UserProfileSerializer(ModelSerializer):
    name = serializers.CharField(source='user.name',
                                 allow_null=True
                                 )
    nickname = serializers.CharField(source='user.nickname',
                                     allow_null=True
                                     )

    class Meta:
        model = UserProfile
        fields = (
            'name',
            'nickname',
            'web_site',
            'introduction',
        )

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        name = user.pop('name')
        nickname = user.pop('nickname')

        super(UserProfileSerializer, self).update(instance, validated_data)

        if name:
            instance.user.name = name
            instance.user.nickname = nickname
            instance.user.save(update_fields=('name', 'nickname',))

        return instance
