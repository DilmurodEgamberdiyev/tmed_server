from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from root.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT
from shared.django.customizations import schema_view

urlpatterns = i18n_patterns(
    # Admin panel
    path('admin/', admin.site.urls),

    # CKEditor
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

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
