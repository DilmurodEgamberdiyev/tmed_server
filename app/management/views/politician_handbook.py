from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Value, OuterRef
from django.db.models.functions import JSONObject, Concat
from rest_framework.generics import ListAPIView

from management.models.politician_handbook import AboutUs, Structure, Law, AboutUsPhoto
from management.serializers import AboutUsSerializer, StructureSerializer, LawSerializer
from root.settings import MEDIA_URL
from shared.django import CustomGenericAPIView, CustomPagination, CKEditorFixMixin


class AboutUsGenericAPIView(CKEditorFixMixin, CustomGenericAPIView):
    """
    GenericAPIView for retrieving 'About Us' entries.
    """
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_queryset(self):
        about_us_with_photos = AboutUs.objects.annotate(
            images=ArraySubquery(AboutUsPhoto.objects.filter(about_us_id=OuterRef('id')).annotate(
                photo_dict=JSONObject(id='id',
                                      url=Concat(Value(self.request.build_absolute_uri('/')), Value(MEDIA_URL),
                                                 'photo'))).values('photo_dict'))
        )
        return about_us_with_photos


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
