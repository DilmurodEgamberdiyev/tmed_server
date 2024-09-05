from modeltranslation.translator import TranslationOptions
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from root.settings import LANGUAGES_KEYS


class CustomTranslationOptions(TranslationOptions):
    required_languages = LANGUAGES_KEYS


class CustomGenericAPIView(GenericAPIView):

    def get_queryset(self):
        """
        Override to return only the first object.
        """
        queryset = self.queryset
        if queryset.exists():
            return queryset[:1]  # Return the first object
        return queryset

    def get_object(self):
        """
        Retrieve the first object from the queryset.
        """
        queryset = self.get_queryset()
        try:
            obj = queryset[0]
        except IndexError:
            raise NotFound("No 'About Us' entry found.")
        return obj

    def get(self, request, *args, **kwargs):
        """
        Handle GET request and return the serialized data.
        """
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
