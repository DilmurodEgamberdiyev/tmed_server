from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import Value, OuterRef, F, CharField, Subquery
from django.db.models.functions import JSONObject, Concat
from django.utils.translation import gettext as _, get_language
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet

from management.models.bms import AppsOrganization
from management.models.oms import AppsSpecialist, AppsCategory
from management.models.pms import AppsProductToOrganization, AppsProductPrice
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
        organizations = AppsOrganization.objects.values('id', 'creator', 'logo', 'name', 'owner',
                                                        'slug_name').annotate(
            logotype=Concat(Value('https://dwed.fra1.digitaloceanspaces.com'), Value('/'), Value(f'BMS/media/'),
                            F('logo'), output_field=CharField()))
        return Response(organizations)

    # @action(detail=True, methods=['get'], url_path='(?P<organization_id>[0-9]+)')
    @staticmethod
    def retrieve(request, org_slug=None):
        try:
            organization = AppsOrganization.objects.values('id', 'creator', 'logo', 'name', 'owner',
                                                           'slug_name').annotate(
                logotype=Concat(Value('https://dwed.fra1.digitaloceanspaces.com'), Value('/'), Value(f'BMS/media/'),
                                F('logo'), output_field=CharField())).get(slug_name=org_slug)
        except AppsOrganization.DoesNotExist:
            return Response({'organization': _('Object not found!')}, HTTP_404_NOT_FOUND)
        return Response(organization)

    @action(detail=True, methods=['get'], url_path='services')
    def products(self, request, org_slug=None):
        """List products of a specific organization"""
        services = AppsProductToOrganization.objects.filter(org=org_slug).annotate(
            table_price=Subquery(AppsProductPrice.objects.filter(
                org_product=OuterRef('id'), active=True)[:1].values('value')),
            currency_price=Subquery(AppsProductPrice.objects.filter(
                org_product=OuterRef('id'), active=True)[:1].values('currency')),
        ).values('id', 'product__name', 'org', 'table_price', 'currency_price')
        return Response(services)

    @action(detail=True, methods=['get'], url_path='services/(?P<product_id>[0-9]+)')
    def product_detail(self, request, org_slug=None, product_id=None):
        """Retrieve details of a specific product by ID for an organization"""
        #         product = pms_client.product_to_org.product_find(
        #             product_id=[int(product_id)], org=org_slug, org_status=True)
        #         return Response(product)
        try:
            service = AppsProductToOrganization.objects.annotate(
                table_price=Subquery(AppsProductPrice.objects.filter(
                    org_product=OuterRef('id'), active=True)[:1].values('value')),
                currency_price=Subquery(AppsProductPrice.objects.filter(
                    org_product=OuterRef('id'), active=True)[:1].values('currency')),
            ).values('id', 'product__name', 'org', 'table_price', 'currency_price').get(org=org_slug, id=product_id)
            return Response(service)
        except AppsProductToOrganization.DoesNotExist:
            return Response({'service': _('Object not found!')}, HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='specialists')
    def specialists(self, request, org_slug=None):
        """List specialists of a specific organization"""
        #         specialists = bms_client.specialist.list_specialist_detailed(filters={'org_slug': org_slug})
        #         return Response(specialists)
        specialists = AppsSpecialist.objects.filter(org=org_slug).select_related('job').annotate(
            position=JSONObject(
                title=AppsCategory.objects.translate(get_language()).filter(id=OuterRef('job_id')).values('name'))
        ).values('id', 'name', 'lastname', 'avatar', 'position')
        return Response(specialists)

    @action(detail=True, methods=['get'], url_path='specialists/(?P<specialist_id>[0-9]+)')
    def specialist_detail(self, request, org_slug=None, specialist_id=None):
        """List specialists of a specific organization"""
        #         specialist = bms_client.specialist.retrieve(id=int(specialist_id))
        #         return Response(specialist)
        try:
            specialist = AppsSpecialist.objects.select_related('job').annotate(
                position=JSONObject(
                    title=AppsCategory.objects.translate(get_language()).filter(id=OuterRef('job_id')).values('name'))
            ).values('id', 'name', 'lastname', 'avatar', 'position').get(org=org_slug, id=specialist_id)
            return Response(specialist)
        except AppsSpecialist.DoesNotExist:
            return Response({'specialist': _('Object not found!')}, HTTP_404_NOT_FOUND)
