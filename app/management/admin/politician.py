from django.contrib.admin import register
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from management.admin.utils import ContentPhotosInline
from management.models import Management, Content
from root.settings import MEDIA_URL
from shared.django import CustomVerboseNamesOfFieldsSortableModelTranslations, CustomImportExportModelAdmin


@register(Management)
class ManagementSortableModelAdmin(CustomVerboseNamesOfFieldsSortableModelTranslations, CustomImportExportModelAdmin):
    list_display = ('id', 'image', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                    'permission')
    list_editable = 'administration_type',

    def image(self, obj):
        url = reverse('admin:management_management_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="/{MEDIA_URL}/%s" width="125" height="125"/></a>' % obj.file)

    image.short_description = _('Image')
    image.admin_order_field = 'file'


@register(Content)
class ContentSortableModelAdmin(CustomVerboseNamesOfFieldsSortableModelTranslations, CustomImportExportModelAdmin):
    list_display = 'id', 'title', 'type', 'image'
    list_editable = 'type',
    inlines = ContentPhotosInline,

    def image(self, obj):
        """
        Display a clickable image that links to the object's detail page in the admin panel.
        """
        try:
            photo_url = obj.main_photo.url
        except ValueError:
            return None
        url = reverse('admin:management_content_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="{photo_url}" width="225" height="225"/></a>')

    image.short_description = _('Image')
    image.admin_order_field = 'image'
