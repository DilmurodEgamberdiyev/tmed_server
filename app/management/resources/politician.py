from import_export.resources import ModelResource

from management.models import Management, Content


class ManagementResource(ModelResource):
    """
    Resource class for managing 'Management' data import/export.
    """

    class Meta:
        model = Management
        fields = ('id', 'file', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                  'permission')
        export_order = ('id', 'file', 'phone_number', 'email', 'administration_type', 'full_name', 'role',
                        'reception_day', 'permission')


class ContentResource(ModelResource):
    class Meta:
        model = Content
        fields = 'title', 'content', 'category', 'main_photo', 'tags'
        export_order = 'title', 'content', 'category', 'main_photo', 'tags'


class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = 'id', 'title'
        export_order = 'id', 'title'
