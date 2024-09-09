from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ChoiceFilter, ModelMultipleChoiceFilter

from management.models import Content


class ContentFilter(FilterSet):
    type = ChoiceFilter(choices=Content.ContentType.choices, label=_('Type'))

    class Meta:
        model = Content
        fields = 'type',
