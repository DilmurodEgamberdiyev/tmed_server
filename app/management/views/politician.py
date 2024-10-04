from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Value, OuterRef
from django.db.models.functions import Concat, JSONObject
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from management.models.politician import Management, Content, ContentPhoto
from management.serializers import ManagementSerializer, ContentListModelSerializer, ContentDetailModelSerializer
from root.settings import MEDIA_URL
from shared.django import CustomPagination, CKEditorFixMixin
from shared.django.filters import ContentFilter
from swagger_content import management_schema, content_schema


@management_schema
class ManagementReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing or retrieving 'Management' entries.
    """
    queryset = Management.objects.all()
    serializer_class = ManagementSerializer
    pagination_class = CustomPagination


@content_schema
class ContentReadOnlyModelViewSet(CKEditorFixMixin, ReadOnlyModelViewSet):
    pagination_class = CustomPagination
    filter_backends = DjangoFilterBackend, SearchFilter
    filterset_class = ContentFilter
    search_fields = 'title',

    def get_queryset(self):
        contents_with_photos = Content.objects.annotate(
            images=ArraySubquery(ContentPhoto.objects.filter(content_id=OuterRef('id')).annotate(
                photo_dict=JSONObject(id='id',
                                      url=Concat(Value(self.request.build_absolute_uri('/')), Value(MEDIA_URL),
                                                 'photo'))).values('photo_dict'))
        )
        return contents_with_photos

    def get_serializer_class(self):
        if self.action == 'list':
            return ContentListModelSerializer
        if self.action == 'retrieve':
            return ContentDetailModelSerializer
        return super().get_serializer_class()
