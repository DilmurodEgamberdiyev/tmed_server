from django.urls import path
from rest_framework.routers import DefaultRouter

from management.views import ManagementReadOnlyModelViewSet, ContentReadOnlyModelViewSet, AboutUsGenericAPIView, \
    StructureListAPIView, LawListAPIView, OrganizationViewSet

# Create a router and register the ViewSet
router = DefaultRouter()
router.register(r'management', ManagementReadOnlyModelViewSet, basename='management')
router.register(r'contents', ContentReadOnlyModelViewSet, basename='content')
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [

                  # about-us
                  path('about-us/', AboutUsGenericAPIView.as_view(), name='about-us'),

                  # structure
                  path('structure/', StructureListAPIView.as_view(), name='structure'),

                  # laws
                  path('laws/', LawListAPIView.as_view(), name='laws'),
              ] + router.urls
