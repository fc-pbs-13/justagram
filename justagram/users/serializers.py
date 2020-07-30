from rest_framework import serializers

from users.models import User, UserProfile
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """
    회원 생성, 회원 탈퇴 Serializer
    """

    class Meta:
        model = User
        fields = (
            'id',
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

    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if not new_password1:
            raise serializers.ValidationError("반드시 입력해야 하는 값입니다.")
        elif not new_password2:
            raise serializers.ValidationError("반드시 입력해야 하는 값입니다.")
        elif data['new_password1'] == data['new_password2']:
            return data
        else:
            raise serializers.ValidationError("비밀번호가 서로 다릅니다.")

    def validate_password(self, value):
        user = self.instance
        if user.check_password(value):
            return value
        raise serializers.ValidationError("잘못된 비밀번호 입니다.")


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
            'password': {'write_only': True}
        }

    def validate(self, data):
        user = self.instance
        if user.check_password(data['password']):
            return data
        else:
            raise serializers.ValidationError("회원정보가 일치하지 않습니다.")


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
            'post_count',
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

        serializer = UserProfileSerializer(data=instance)
        serializer.is_valid()

        instance.user.save(update_fields=('name', 'username',))

        return instance
