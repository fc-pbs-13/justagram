from rest_framework import status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from users.models import User, UserProfile
from users.serializers import UserSignupSerializer, UserSignSerializer, UserProfileSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    회원 가입, 회원 탈퇴 View
    """
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()


class UserSignViewSet(GenericViewSet):
    """
    로그인, 로그아웃 View
    """
    queryset = User.objects.all()
    serializer_class = UserSignSerializer

    @action(methods=['post'], detail=False)
    def signin(self, request, *args, **kwargs):
        email = User.objects.get(email=request.data['email'])
        password = request.data['password']
        if email.check_password(password):
            token, create = Token.objects.get_or_create(user=email)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=False)
    def signout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]
