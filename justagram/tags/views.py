from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
