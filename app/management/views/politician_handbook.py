from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Value, OuterRef
from django.db.models.functions import JSONObject, Concat
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from management.grpc_clients import bms_client, pms_client
from management.models.politician_handbook import AboutUs, Structure, Law, AboutUsPhoto
from management.serializers import AboutUsSerializer, StructureSerializer, LawSerializer
from root.settings import MEDIA_URL
from shared.django import CustomGenericAPIView, CustomPagination, CKEditorFixMixin
from swagger_content import about_us_schema, structure_schema, law_schema, organizations_schema


@about_us_schema
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


@structure_schema
class StructureListAPIView(ListAPIView):
    """
    ListAPIView for listing 'About Us' entries.
    """
    queryset = Structure.objects.all()
    serializer_class = StructureSerializer
    pagination_class = CustomPagination


@law_schema
class LawListAPIView(ListAPIView):
    """
    ListAPIView for listing 'Law' entries.
    """
    queryset = Law.objects.all()
    serializer_class = LawSerializer
    pagination_class = CustomPagination


@organizations_schema
class OrganizationViewSet(GenericViewSet):
    lookup_field = 'org_slug'

    @staticmethod
    def list(request):
        """List all organizations"""
        organizations = bms_client.organization.list()
        return Response(organizations)

    # @action(detail=True, methods=['get'], url_path='(?P<organization_id>[0-9]+)')
    @staticmethod
    def retrieve(request, org_slug=None):
        organization = bms_client.organization.retrieve(slug_name=org_slug)
        return Response(organization)

    @action(detail=True, methods=['get'], url_path='services')
    def products(self, request, org_slug=None):
        """List products of a specific organization"""
        products = pms_client.product_to_org.list(org=org_slug, org_status=True)
        return Response(products)

    @action(detail=True, methods=['get'], url_path='services/(?P<product_id>[0-9]+)')
    def product_detail(self, request, org_slug=None, product_id=None):
        """Retrieve details of a specific product by ID for an organization"""
        product = pms_client.product_to_org.product_find(
            product_id=[int(product_id)], org=org_slug, org_status=True)
        return Response(product)

    @action(detail=True, methods=['get'], url_path='specialists')
    def specialists(self, request, org_slug=None):
        """List specialists of a specific organization"""
        specialists = bms_client.specialist.list_specialist_detailed(filters={'org_slug': org_slug})
        return Response(specialists)

    @action(detail=True, methods=['get'], url_path='specialists/(?P<specialist_id>[0-9]+)')
    def specialist_detail(self, request, org_slug=None, specialist_id=None):
        """List specialists of a specific organization"""
        specialist = bms_client.specialist.retrieve(id=int(specialist_id))
        return Response(specialist)
