from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from stories.models import Story, CheckShow
from stories.serializers import StorySerializer, CheckShowSerializer
from users.models import User


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            CheckShow.objects.get_or_create(
                show_user=self.request.user,
                show_story=Story.objects.get(id=kwargs['pk']),
            )

        return response

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def get_queryset(self):
        time = timezone.now() - timedelta(days=1)
        user = self.request.user
        qs = User.objects.filter(to_follow_user__from_follow_user_id=user.id,
                                 to_follow_user__related_type='f')
        qs = Story.objects.filter(Q(user__in=qs) | Q(user=user), time__gte=time)
        return qs


class CheckShowViewSet(viewsets.ModelViewSet):
    queryset = CheckShow
    serializer_class = CheckShowSerializer
