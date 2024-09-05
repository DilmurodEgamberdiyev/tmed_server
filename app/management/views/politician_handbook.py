from rest_framework.generics import ListAPIView

from management.models.politician_handbook import AboutUs, Structure, Law
from management.serializers import AboutUsSerializer, StructureSerializer, LawSerializer
from shared.django import CustomGenericAPIView, CustomPagination


class AboutUsGenericAPIView(CustomGenericAPIView):
    """
    GenericAPIView for retrieving 'About Us' entries.
    """
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer


class StructureListAPIView(ListAPIView):
    """
    ListAPIView for listing 'About Us' entries.
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    pagination_class = CustomPagination


class LawListAPIView(ListAPIView):
    """
    ListAPIView for listing 'Law' entries.
    """
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    pagination_class = CustomPagination
