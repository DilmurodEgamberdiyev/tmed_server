from django.contrib.admin import register
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from rest_framework.reverse import reverse

from management.models import Management, Content
from root.settings import MEDIA_URL
from shared.django import CustomVerboseNamesOfFieldsModelTranslations


@register(Management)
class ManagementModelAdmin(CustomVerboseNamesOfFieldsModelTranslations, ImportExportModelAdmin):
    list_display = ('id', 'image', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                    'job_description', 'permission')
    list_editable = 'administration_type',

    def image(self, obj):
        url = reverse('admin:management_management_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="/{MEDIA_URL}/%s" width="125" height="125"/></a>' % obj.file)

    image.short_description = _('Image')
    image.admin_order_field = 'file'


# @register(Category)
# class CategoryModelAdmin(CustomVerboseNamesOfFieldsModelTranslations, ImportExportModelAdmin):
#     list_display = 'title',


@register(Content)
class PostModelAdmin(CustomVerboseNamesOfFieldsModelTranslations, ImportExportModelAdmin):
    list_display = 'id', 'title', 'type', 'image'
    filter_horizontal = 'tags',
    list_editable = 'type',

    def image(self, obj):
        """
        Display a clickable image that links to the object's detail page in the admin panel.
        """
        url = reverse('admin:management_content_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="{obj.main_photo.url}" width="225" height="225"/></a>')

    image.short_description = _('Image')
    image.admin_order_field = 'image'
