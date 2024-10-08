from re import split

from django.utils.html import strip_tags
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from management.models.politician import Management, Content
from root.settings import MEDIA_URL


class ManagementSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'Management' entry.
    """

    class Meta:
        model = Management
        fields = ('id', 'file', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                  'job_description', 'permission')


class ContentListModelSerializer(ModelSerializer):
    short_description = SerializerMethodField()
    images = SerializerMethodField()

    def to_representation(self, instance):
        instance.content = instance.content.replace(f'="/{MEDIA_URL}', f"=\"{self.context.get('MEDIA_URL')}")
        return super().to_representation(instance)

    class Meta:
        model = Content
        fields = 'id', 'title', 'type', 'main_photo', 'short_description', 'images', 'created_at', 'updated_at'

    @extend_schema_field(CharField)
    def get_short_description(self, obj):
        # Strip HTML tags from content
        plain_text = strip_tags(obj.content)

        # Split the content into sentences and return the first two
        sentences = split(r'(?<=[.!?]) +', plain_text)  # Split by punctuation followed by a space
        first_two_sentences = ' '.join(sentences[:2])  # Get the first two sentences

        return first_two_sentences

    @extend_schema_field(CharField)
    def get_images(self, obj):
        return obj.images


class ContentDetailModelSerializer(ModelSerializer):
    images = SerializerMethodField()

    def to_representation(self, instance):
        instance.content = instance.content.replace(f'="/{MEDIA_URL}', f"=\"{self.context.get('MEDIA_URL')}")
        return super().to_representation(instance)

    class Meta:
        model = Content
        fields = 'id', 'title', 'type', 'content', 'main_photo', 'images', 'created_at', 'updated_at'

    @extend_schema_field(CharField)
    def get_images(self, obj):
        return obj.images
