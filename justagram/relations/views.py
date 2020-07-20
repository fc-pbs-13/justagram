from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from relations.models import Follow
from relations.serializers import FollowSerializer
from users.models import User


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        to_follow_user = get_object_or_404(User, id=self.kwargs.get('profile_pk'))
        serializer.save(
            from_follow_user=self.request.user,
            to_follow_user=to_follow_user
        )

    def get_serializer_context(self):
        context = super(FollowViewSet, self).get_serializer_context()
        context['action'] = self.action
        return context
