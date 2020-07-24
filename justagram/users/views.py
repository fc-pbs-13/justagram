from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwner, IsAnonymous
from users.models import User, UserProfile
from users.serializers import UserSerializer, UserSignSerializer, UserProfileSerializer, UserPasswordSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    회원 가입, 회원 탈퇴, 로그인, 로그아웃 view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.action == 'login':
            return UserSignSerializer
        elif self.action == 'change_password':
            return UserPasswordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [IsAnonymous()]
        return super().get_permissions()

    @action(methods=['put'], detail=True, )
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = request.data['new_password1']
        request.user.password = new_password
        request.user.save()

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        token, create = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=status.HTTP_201_CREATED
                        )

    @action(methods=['delete'], detail=False)
    def logout(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserPasswordViewSet(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    """
    Show Profile, Update Profile View
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['get'], detail=True)
    def show_following(self, request, *args, **kwargs):
        user = User.objects.filter(to_follow_user__from_follow_user=kwargs['pk'],
                                   to_follow_user__related_type='f')
        serializers = UserSerializer(user, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def show_follower(self, request, *args, **kwargs):
        print(kwargs)
        user = User.objects.filter(from_follow_user__to_follow_user=kwargs['pk'], )
        serializers = UserSerializer(user, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def show_block(self, request, *args, **kwargs):
        user = User.objects.filter(to_follow_user__from_follow_user=kwargs['pk'],
                                   to_follow_user__related_type='b')
        serializers = UserSerializer(user, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
