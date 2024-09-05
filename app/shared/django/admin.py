from modeltranslation.admin import TranslationAdmin


class CustomVerboseNamesOfFieldsModelTranslations(TranslationAdmin):
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
