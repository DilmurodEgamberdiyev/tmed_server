from import_export.resources import ModelResource

from management.models import AboutUs, Structure, Law


class AboutUsResource(ModelResource):
    """
    Resource class for managing 'About Us' data import/export.
    """

    class Meta:
        model = AboutUs
        fields = 'id', 'description', 'main_photo'
        export_order = 'id', 'description', 'main_photo'


class StructureResource(ModelResource):
    """
    Resource class for managing 'Structure' data import/export.
    """

    class Meta:
        model = Structure
        fields = 'id', 'image'
        export_order = 'id', 'image'


class LawResource(ModelResource):
    """
    Resource class for managing 'Law' data import/export.
    """

    class Meta:
        model = Law
        fields = 'id', 'file', 'name', 'law_type', 'link'
        export_order = 'id', 'file', 'name', 'law_type', 'link'


class TagsResource(ModelResource):
    class Meta:
        model = Tags
        fields = 'id', 'name'
        export_order = 'id', 'name'
