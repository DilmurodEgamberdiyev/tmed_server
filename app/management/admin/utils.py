from adminsortable2.admin import SortableStackedInline

from management.models import AboutUsPhoto, ContentPhoto


class AboutUsPhotosInline(SortableStackedInline):
    model = AboutUsPhoto
    extra = 1


class ContentPhotosInline(SortableStackedInline):
    model = ContentPhoto
    extra = 1
