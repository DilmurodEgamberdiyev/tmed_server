from modeltranslation.translator import register

from management.models import AboutUs, Law, Management, Tags, Content
from shared.django import CustomTranslationOptions


@register(AboutUs)
class AboutUsTranslationOptions(CustomTranslationOptions):
    fields = 'description',


@register(Law)
class LawTranslationOptions(CustomTranslationOptions):
    fields = 'name',


@register(Management)
class ManagementTranslationOptions(CustomTranslationOptions):
    fields = 'full_name', 'role', 'reception_day', 'job_description', 'permission'


@register(Tags)
class TagsTranslationOptions(CustomTranslationOptions):
    fields = 'title',


@register(Content)
class PostTranslationOptions(CustomTranslationOptions):
    fields = 'title', 'content'
