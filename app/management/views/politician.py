from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from management.models.politician import Management, Content
from management.serializers import ManagementSerializer, PostListModelSerializer, PostDetailModelSerializer
from shared.django import CustomPagination
from shared.django.filters import ContentFilter


class ManagementReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing or retrieving 'Management' entries.
    """
    queryset = Management.objects.all()
    serializer_class = ManagementSerializer
    pagination_class = CustomPagination


class ContentReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Content.objects.all()
    pagination_class = CustomPagination
    filter_backends = DjangoFilterBackend, SearchFilter
    filterset_class = ContentFilter
    search_fields = 'title',

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListModelSerializer
        if self.action == 'retrieve':
            return PostDetailModelSerializer
        return super().get_serializer_class()
