from rest_framework.viewsets import ReadOnlyModelViewSet

from management.models.politician import Management
from management.serializers import ManagementSerializer
from shared.django import CustomPagination


class ManagementReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for listing or retrieving 'Management' entries.
    """
    queryset = Management.objects.all()
    serializer_class = ManagementSerializer
    pagination_class = CustomPagination
