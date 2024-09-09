from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from management.models.politician_handbook import AboutUs, Structure, Law


class AboutUsSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'About Us' entry.
    """
    images = SerializerMethodField()

    class Meta:
        model = AboutUs
        fields = 'id', 'description', 'main_photo', 'images'

    @staticmethod
    def get_images(obj):
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
