from rest_framework.generics import GenericAPIView

from root.settings import MEDIA_URL


class CKEditorFixMixin(GenericAPIView):
    def get_serializer_context(self):
        context_data = super().get_serializer_context()
        context_data['MEDIA_URL'] = self.request.build_absolute_uri('/') + MEDIA_URL
        return context_data
