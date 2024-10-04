from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from management.models.politician_handbook import AboutUs, Structure, Law
from root.settings import MEDIA_URL


class AboutUsSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'About Us' entry.
    """
    images = SerializerMethodField()

    def to_representation(self, instance):
        instance.description = instance.description.replace(f'="/{MEDIA_URL}', f"=\"{self.context.get('MEDIA_URL')}")
        return super().to_representation(instance)

    class Meta:
        model = AboutUs
        fields = 'id', 'description', 'main_photo', 'images'

    @extend_schema_field(CharField)
    def get_images(self, obj):
        return obj.images


class StructureSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'Structure' entry.
    """

    class Meta:
        model = Structure
        fields = 'id', 'image'


class LawSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'Law' entry.
    """

    class Meta:
        model = Law
        fields = 'id', 'file', 'name', 'law_type', 'link'
