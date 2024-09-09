from django.db.models import Model, DateTimeField, PositiveIntegerField
from django.utils.translation import gettext_lazy as _


class TimeAndOrderBaseModel(Model):
    created_at = DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = DateTimeField(_('updated_at'), auto_now=True)
    order = PositiveIntegerField(_('order'), default=0, db_index=True)

    class Meta:
        ordering = 'order',
        abstract = True
