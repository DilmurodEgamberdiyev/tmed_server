from rest_framework.serializers import ModelSerializer

from management.models.politician import Management


class ManagementSerializer(ModelSerializer):
    """
    Serializer for retrieving detailed 'Management' entry.
    """

    class Meta:
        model = Management
        fields = ('id', 'file', 'phone_number', 'email', 'administration_type', 'full_name', 'role', 'reception_day',
                  'job_description', 'permission')
