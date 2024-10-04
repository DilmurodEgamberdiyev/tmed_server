from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from root.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT

urlpatterns = i18n_patterns(
    # Admin panel
    path('admin/', admin.site.urls),

    # CKEditor
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    # Swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # i18n support
    path("i18n/", include("django.conf.urls.i18n")),

    # management
    path('api/v1/', include('management.urls'), name='management')
)

# Static and Media URLs if DEBUG is enabled
if DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    ]
    urlpatterns += debug_toolbar_urls()
