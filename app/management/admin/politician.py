from django.contrib.admin import register
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from rest_framework.reverse import reverse

from management.models import Management
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
