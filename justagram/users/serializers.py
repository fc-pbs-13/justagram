from rest_framework import serializers

from posts.models import Post
from users.models import User, UserProfile
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    회원 생성, 회원 탈퇴 Serializer
    """

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserPasswordSerializer(ModelSerializer):
    new_password1 = serializers.CharField(max_length=128,
                                          required=False)
    new_password2 = serializers.CharField(max_length=128,
                                          required=False)

    class Meta:
        model = User
        fields = (
            'password',
            'new_password1',
            'new_password2',
        )
        extra_kwargs = {
            'new_password1': {'write_only': True},
            'new_password2': {'write_only': True}
        }


class UserSignSerializer(ModelSerializer):
    """
    로그인 Serializer
    """

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
    """
    프로필 Serializer
    """
    name = serializers.CharField(source='user.name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = (
            'name',
            'username',
            'web_site',
            'introduction',
            'following_count',
            'follower_count',
            'post_count',
        )
        read_only_fields = (
            'following_count',
            'follower_count',
        )

    def update(self, instance, validated_data):
        """
        web_sit, introduction update to UserProfile
        name, username update to User
        """
        user = validated_data.pop('user')
        name = user.pop('name')
        username = user.pop('username')

        super().update(instance, validated_data)

        instance.user.name = name
        instance.user.username = username
        instance.user.save(update_fields=('name', 'username',))

        return instance
