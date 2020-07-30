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

    def get_queryset(self):
        queryset = Tag.objects.all()
        tag_name = self.request.query_params.get('tag_name', None)

        if tag_name:
            queryset = Tag.objects.filter(tag_name__startswith=tag_name)

        return queryset
