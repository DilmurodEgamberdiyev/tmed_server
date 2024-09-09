from django.db.models import Model, DateTimeField
from django.utils.translation import gettext_lazy as _


class TimeBaseModel(Model):
    created_at = DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = DateTimeField(_('updated_at'), auto_now=True)

    class Meta:
        abstract = True
