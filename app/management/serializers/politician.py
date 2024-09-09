from re import split

from django.utils.html import strip_tags
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from management.models.politician import Management, Content


class ManagementSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'Management' entry.
    """

    class Meta:
        model = Management
        fields = ('id', 'file', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                  'job_description', 'permission')


class PostListModelSerializer(ModelSerializer):
    short_description = SerializerMethodField()

    class Meta:
        model = Content
        fields = 'id', 'title', 'type', 'main_photo', 'tags', 'short_description'

    @staticmethod
    def get_short_description(obj):
        # Strip HTML tags from content
        plain_text = strip_tags(obj.content)

        # Split the content into sentences and return the first two
        sentences = split(r'(?<=[.!?]) +', plain_text)  # Split by punctuation followed by a space
        first_two_sentences = ' '.join(sentences[:2])  # Get the first two sentences

        return first_two_sentences


class PostDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = 'id', 'title', 'type', 'content', 'main_photo', 'tags'
