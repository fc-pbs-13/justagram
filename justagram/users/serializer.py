from rest_framework.serializers import ModelSerializer

from users.models import UserInfo, UserProfile


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            'email',
            'name',
            'nickname',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'website',
            'introduction',
        )
