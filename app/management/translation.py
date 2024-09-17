from modeltranslation.translator import register

from management.models import AboutUs, Law, Management, Content
from shared.django import CustomTranslationOptions


@register(AboutUs)
class AboutUsTranslationOptions(CustomTranslationOptions):
    fields = 'description',


@register(Law)
class LawTranslationOptions(CustomTranslationOptions):
    fields = 'name',


@register(Management)
class ManagementTranslationOptions(CustomTranslationOptions):
    fields = 'full_name', 'role', 'reception_day', 'permission'


@register(Content)
class PostTranslationOptions(CustomTranslationOptions):
    fields = 'title', 'content'
