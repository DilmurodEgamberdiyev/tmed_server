from django.contrib.admin import register
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from management.admin.utils import AboutUsPhotosInline
from management.models import AboutUs, Structure, Law
from shared.django import CustomVerboseNamesOfFieldsModelTranslations


@register(AboutUs)
class AboutUsModelAdmin(CustomVerboseNamesOfFieldsModelTranslations, ImportExportModelAdmin):
    list_display = 'id', 'photo_link', 'description'
    inlines = AboutUsPhotosInline,

    def photo_link(self, obj):
        """
        Display a clickable image that links to the object's detail page in the admin panel.
        """
        try:
            photo_url = obj.main_photo.url
        except ValueError:
            return None
        url = reverse('admin:management_aboutus_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="{photo_url}" width="125" height="125"/></a>')

    photo_link.short_description = _('Image')
    photo_link.admin_order_field = 'image'

    def has_add_permission(self, request):
        """
        Prevent adding new instances if one already exists.
        """
        if AboutUs.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of the existing instance.
        """
        return False


@register(Structure)
class StructureModelAdmin(ImportExportModelAdmin):
    list_display = 'id', 'photo_link'

    # fields = 'image', 'old_image'
    # readonly_fields = 'old_image',

    def photo_link(self, obj):
        """
        Display a clickable image that links to the object's detail page in the admin panel.
        """
        url = reverse('admin:management_structure_change', args=[obj.id])
        return mark_safe(f'<a href="{url}"><img src="{obj.image.url}" width="125" height="125"/></a>')

    photo_link.short_description = _('Image')
    photo_link.admin_order_field = 'image'

    # def old_image(self, obj):
    #     return mark_safe(f'<img src="{obj.image.url}"/>')

    # old_image.short_description = _('Old image')


@register(Law)
class LawModelAdmin(CustomVerboseNamesOfFieldsModelTranslations, ImportExportModelAdmin):
    list_display = 'id', 'name', 'file', 'law_type', 'special_link'
    list_editable = 'law_type',

    @staticmethod
    def special_link(obj):
        """
        Display a clickable image that links to the object's detail page in the admin panel.
        """
        return mark_safe(f'<a href="{obj.link}">{obj.link}</a>')

    special_link.short_description = _('Link')
    special_link.admin_order_field = 'link'
