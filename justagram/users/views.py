from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from follows.models import Follow
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

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'login':
            return UserSignSerializer
        elif self.action == 'change_password':
            return UserPasswordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'login':
            return [AllowAny()]
        return super().get_permissions()

    @action(methods=['put'], detail=True, )
    def change_password(self, request, *args, **kwargs, ):
        instance = request.user
        serializer = self.get_serializer(instance,
                                         data=request.data)
        serializer.is_valid()
        password = request.data['password']

        if instance.check_password(password):
            request_data = request.data
            new_password1 = request_data['new_password1']
            new_password2 = request_data['new_password2']

            if new_password1 == new_password2:
                request.user.password = new_password1
                request.user.save()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        email = User.objects.get(email=request.data['email'])
        password = request.data['password']

        if email.check_password(password):
            token, create = Token.objects.get_or_create(user=email)
            return Response({'token': token.key},
                            status=status.HTTP_201_CREATED
                            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

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
    def follow(self, request, *args, **kwargs):
        user = User.objects.filter(to_follow_user__from_follow_user=request.user,
                                   to_follow_user__related_type='f')
        serializers = UserSerializer(user, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def block(self, request, *args, **kwargs):
        user = User.objects.filter(to_follow_user__from_follow_user=request.user,
                                   to_follow_user__related_type='b')
        serializers = UserSerializer(user, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
