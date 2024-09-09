from django.contrib.admin import StackedInline

from management.models import AboutUsPhoto, ContentPhoto


class AboutUsPhotosInline(StackedInline):
    model = AboutUsPhoto
    extra = 1


class ContentPhotosInline(StackedInline):
    model = ContentPhoto
    extra = 1
