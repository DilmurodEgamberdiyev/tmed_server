from adminsortable2.admin import SortableAdminMixin
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin


class CustomSortableAdminMixin(SortableAdminMixin):
    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))

        # Remove '_reorder_' if it's already in the list to avoid duplicates
        if '_reorder_' in list_display:
            list_display.remove('_reorder_')

        # Add '_reorder_' to the end of the list
        list_display.append('_reorder_')

        return list_display


class CustomVerboseNamesOfFieldsSortableModelTranslations(CustomSortableAdminMixin, TranslationAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        language_labels = {
            'ru': {'_en': ' на английском', '_ru': ' на русском', '_uz': ' на узбекском'},
            'uz': {'_en': ' ingliz tilida', '_ru': ' rus tilida', '_uz': " o'zbek tilida"},
            'en': {'_en': ' in english', '_ru': ' in russian', '_uz': " in uzbek"}
        }

        current_language_code = request.LANGUAGE_CODE
        for field_name, field in form.base_fields.items():
            lang_code = field_name[-3:]
            new_label_text = field.label
            if lang_code in language_labels[current_language_code]:
                new_label_text += language_labels[current_language_code][lang_code]
                new_label_text = new_label_text.replace(f"[{lang_code[1:]}]", '')
            field.label = new_label_text

        return form


class CustomImportExportModelAdmin(ImportExportModelAdmin):

    def init_change_list_template(self):
        # Store already set change_list_template to allow users to independently
        # customize the change list object tools. This treats the cases where
        # `self.change_list_template` is `None` (the default in `ModelAdmin`) or
        # where `self.import_export_change_list_template` is `None` as falling
        # back on the default templates.
        if getattr(self, "change_list_template", None):
            self.ie_base_change_list_template = self.change_list_template
        else:
            self.ie_base_change_list_template = "admin/change_list.html"

        try:
            self.change_list_template = getattr(
                self, "import_export_change_list_template", None
            )
        except AttributeError:
            pass

        if self.change_list_template is None:
            self.change_list_template = self.ie_base_change_list_template
