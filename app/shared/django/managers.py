import datetime

from django.apps import apps
from django.db.models import F, OuterRef, Prefetch, Subquery, Count, Sum, ImageField, QuerySet, Max
from django.db.models.expressions import RawSQL
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor, ReverseManyToOneDescriptor
from django.db.models.functions import Coalesce
from django.db.models.manager import BaseManager
from django.db.models.query_utils import DeferredAttribute, Q


def get_manager(*names):
    MANAGERS = {
        'translate': TranslateQuerySetMixin,
        'filter_recursive': RecursionFindQuerySetMixin,
        'statistic_order': StatisticsOrderMixin,
        'statistic_product_to_order': StatisticsProductToOrderMixin,
        'image': ImageMixin,
        'statistic_category': StatisticsCategoryMixin,
        'statistic_user': StatisticsUserMixin,
        'statistic_specialist': StatisticsSpecialistMixin,
    }
    qs_list = [value for key, value in MANAGERS.items() if key in names]

    class QS(QuerySet, *qs_list):
        pass

    class Manager(BaseManager.from_queryset(QS)):
        pass

    return Manager()


def _find_foreign_field_name(from_model, to_field_model):
    for key, value in from_model.__dict__.items():
        if isinstance(value, ForwardManyToOneDescriptor):
            if to_field_model == value.field.remote_field.model:
                return key
    assert False, f"Invalid  '{from_model.__name__}' model. " \
                  f"Can not find foregin field to {to_field_model.__name__}"


def _find_releted_field_name(from_model, to_field_model):
    for key, value in from_model.__dict__.items():
        if isinstance(value, ReverseManyToOneDescriptor):
            if to_field_model == value.field.model:
                return key
    assert False, f"Invalid  '{from_model.__name__}' model. " \
                  f"Can not find releted field to {to_field_model.__name__}"


def get_model(model):
    return apps.get_model('management', model) if isinstance(model, str) else model


class TranslateQuerySetMixin:

    def translate(self, lang, **kwargs):
        if not getattr(self.model, 'TRANSLATE_FIELDS', None):
            return self
        annotate_fields = dict()
        prefetch_fields = list()
        for field_name in self.model.TRANSLATE_FIELDS:
            if isinstance(getattr(self.model, field_name, None), DeferredAttribute):  # Field
                assert getattr(self.model, 'TRANSLATE_MODEL', None), \
                    f"TRANSLATE_MODEL not found from {self.model.__name__}"
                translate_model = get_model(self.model.TRANSLATE_MODEL)
                lookup_field = _find_foreign_field_name(translate_model, self.model)
                assert lookup_field, \
                    f"Invalid  TRANSLATE_MODEL '{translate_model.__name__}' " \
                    f"in model '{self.model.__name__}'"
                annotate_fields.update(
                    {
                        f'tr_{field_name}': Coalesce(
                            Subquery(
                                translate_model.objects.filter(
                                    **{
                                        lookup_field: OuterRef('id'),
                                    },
                                    lang=lang
                                ).values(field_name)
                            ),
                            F(field_name)
                        ),
                    }
                )
            elif isinstance(getattr(self.model, field_name, None), ForwardManyToOneDescriptor):  # Foreign field
                prefetch_fields.append(
                    Prefetch(
                        field_name,
                        queryset=getattr(self.model, field_name).field.remote_field.model.objects.translate(lang)
                    )
                )
            elif isinstance(getattr(self.model, field_name, None), ReverseManyToOneDescriptor):  # Releted field
                prefetch_fields.append(
                    Prefetch(
                        field_name,
                        queryset=getattr(self.model, field_name).field.model.objects.translate(lang)
                    )
                )
        prefetch_related = kwargs.get("prefetch_related", []) + prefetch_fields
        prefetch_related = sorted(prefetch_related, key=lambda a: a.prefetch_to if isinstance(a, Prefetch) else a)
        return self.annotate(**annotate_fields).prefetch_related(*prefetch_related)


class ImageMixin:

    def annotate_remote_image(self, name=None):
        if not getattr(self.model, 'IMAGE_MODELS', None):
            return self
        annotate_fields = dict()

        for image_model_name in self.model.IMAGE_MODELS:
            image_model = apps.get_model('apps', image_model_name)
            assert hasattr(image_model, 'RESIZE_MODEL'), \
                f'{self.model.__name__} model invalid IMAGE_MODELS ({image_model.__name__}). ' \
                f'IMAGE_MODELS must be contain extened model from CreateResizeImagesModel'

            lookup_field = _find_foreign_field_name(image_model, self.model)
            list_of_image_fields = [field.name for field in image_model._meta.fields if type(field) == ImageField]
            list_of_resize_image_fields = [field.name for field in
                                           image_model.RESIZE_MODEL._meta.fields if type(field) == ImageField]
            _original_field_name = _find_foreign_field_name(image_model.RESIZE_MODEL, image_model)
            for image_field in list_of_image_fields:
                if image_field not in list_of_resize_image_fields:
                    continue
                annotate_fields.update(**{
                    f'image_{image_model_name.lower()}': Coalesce(
                        Subquery(image_model.RESIZE_MODEL.objects.filter(**{
                            f'{_original_field_name}__{lookup_field}_id': OuterRef('id'),
                            f"{_original_field_name}__main": True,
                            'name': name
                        })[:1].values(image_field)),
                        Subquery(image_model.objects.filter(**{
                            f'{lookup_field}_id': OuterRef('id'),
                            'main': True,
                        })[:1].values(image_field)),
                    )
                })

            return self.annotate(**annotate_fields)

    def annotate_image(self, name=None):
        annotate_fields = dict()
        original_model = self.model
        assert hasattr(original_model, 'RESIZE_MODEL'), \
            f'{original_model.__name__} model invalid IMAGE_MODELS ({original_model.__name__}). ' \
            f'IMAGE_MODELS must be contain extened model from CreateResizeImagesModel'
        resize_model = original_model.RESIZE_MODEL

        list_of_image_fields = [field.name for field in original_model._meta.fields if type(field) == ImageField]
        list_of_resize_image_fields = [field.name for field in
                                       resize_model._meta.fields if type(field) == ImageField]
        for image_field in list_of_image_fields:
            if image_field not in list_of_resize_image_fields:
                continue
            _original_field_name = _find_foreign_field_name(resize_model, original_model)
            annotate_fields.update(
                {f'resized_{image_field}':
                    Coalesce(
                        Subquery(resize_model.objects.filter(**{f'{_original_field_name}_id': OuterRef('id'),
                                                                'name': name}
                                                             )[:1].values(image_field)),
                        F(image_field)
                    )})
        return self.annotate(**annotate_fields)


class RecursionFindQuerySetMixin:

    def filter_recursive(self, **kwargs):
        fields = _find_foreign_field_name(self.model, self.model)
        table = f'{self.model._meta.app_label}_{self.model.__name__.lower()}'
        sql, params = self.filter(**kwargs).values('id').query.sql_with_params()
        params = tuple([f"'{p}'" if isinstance(p, str) else p for p in params])
        return self.filter(id__in=RawSQL(
            f"""
            WITH RECURSIVE r AS (
                SELECT id, parent_id, name, status
                FROM {table}
                WHERE id IN ({sql % params})
                UNION ALL
                SELECT {table}.id, {table}.parent_id, {table}.name, {table}.status
                FROM {table}
                     JOIN r
                          ON {' OR '.join([f'{table}.{field}_id = r.id' for field in fields])}
            )
            SELECT id FROM r""", ()
        ))


class StatisticsOrderMixin:
    request = None

    def sum_count_annotate(self):
        return self.annotate(
            total_clients_count=Count('user_id', distinct=True),
            coupon_clients_count=Count('user_id', distinct=True, filter=Q(producttoorder__coupon__isnull=False)),
            full_price_clients_count=Count('user_id', distinct=True, filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_count=Count('id', distinct=True),
            coupon_orders_count=Count('id', distinct=True, filter=Q(producttoorder__coupon__isnull=False)),
            full_price_orders_count=Count('id', distinct=True, filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost')), 0.),
            coupon_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost'),
                                            filter=Q(producttoorder__coupon__isnull=False)), 0.),
            full_price_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost'),
                                                filter=Q(producttoorder__coupon__isnull=True)), 0.)
        )

    def responsible_plan_annotate(self, date_from=None, date_end=None):
        return self._plan_filter(date_from, date_end, specialist_id=OuterRef('responsible_id'))

    def directed_specialist_plan_annotate(self, date_from=None, date_end=None):
        return self._plan_filter(date_from, date_end, specialist_id=OuterRef('directed_specialist_id'))

    def responsible_cat_plan_annotate(self, date_from=None, date_end=None):
        return self._plan_filter(date_from, date_end, specialist__spec_cat_id=OuterRef('responsible__spec_cat_id'))

    def directed_specialist_cat_plan_annotate(self, date_from=None, date_end=None):
        return self._plan_filter(date_from, date_end,
                                 specialist__spec_cat_id=OuterRef('directed_specialist__spec_cat_id'))

    def _plan_filter(self, date_from=None, date_end=None, **kwargs):
        from management.models.oms import AppsPlanHistory

        date_from = datetime.datetime.now().date() - datetime.timedelta(1) \
            if date_from is None else datetime.datetime.strptime(date_from, '%Y-%m-%dT%H:%M:%S').date()
        date_end = datetime.datetime.now() \
            if date_end is None else datetime.datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S')

        if date_end.hour > 12:
            date_end += datetime.timedelta(1)
        date_end = date_end.date()

        return self.annotate(
            plan_orders_cost=Coalesce(Subquery(
                AppsPlanHistory.objects.filter(
                    **kwargs,
                    date__gt=date_from, date__lt=date_end,
                    type=1
                ).values('specialist_id').annotate(
                    plan_orders_cost=Sum('value'),
                ).values('plan_orders_cost')
            ), 0.),
            plan_clients_count=Coalesce(Subquery(
                AppsPlanHistory.objects.filter(
                    **kwargs,
                    date__gt=date_from, date__lt=date_end,
                    type=2
                ).values('specialist_id').annotate(
                    plan_clients_count=Sum('value'),
                ).values('plan_clients_count')
            ), 0.)
        )

    def total_sum_count_aggragate(self):
        return self.aggregate(
            total_clients_count_sum=Count('user_id', distinct=True),
            coupon_clients_count_sum=Count('user_id', distinct=True,
                                           filter=Q(producttoorder__coupon__isnull=False)),
            full_price_clients_count_sum=Count('user_id', distinct=True,
                                               filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_count_sum=Sum('total_orders_count'),
            coupon_orders_count_sum=Sum('coupon_orders_count'),
            full_price_orders_count_sum=Sum('full_price_orders_count'),
            total_orders_cost_sum=Sum('total_orders_cost'),
            coupon_orders_cost_sum=Sum('coupon_orders_cost'),
            full_price_orders_cost_sum=Sum('full_price_orders_cost'),
        )


class StatisticsProductToOrderMixin:
    request = None

    def sum_count_annotate(self):
        return self.annotate(
            total_orders_qty_sum=Sum('qty'),
            total_product_count=Count('product', distinct=True),
            total_orders_count=Count('order_id', distinct=True),
            total_orders_cost=Coalesce(Sum(F('qty') * F('cost')), 0.),
            coupon_orders_cost=Coalesce(Sum(F('qty') * F('cost'),
                                            filter=Q(coupon__isnull=False)), 0.),
            full_price_orders_cost=Coalesce(Sum(F('qty') * F('cost'),
                                                filter=Q(coupon__isnull=True)), 0.),
            coupon_orders_count=Count('id', filter=Q(coupon__isnull=False), distinct=True),
            full_price_orders_count=Count('id', filter=Q(coupon__isnull=True), distinct=True),
            total_clients_count=Count('order__user_id', distinct=True),
            coupon_clients_count=Count('order__user_id', distinct=True, filter=Q(coupon__isnull=False)),
            full_price_clients_count=Count('order__user_id', distinct=True, filter=Q(coupon__isnull=True)),
            last_order_date=Max('order__create_date__date'),
            debt=Coalesce(F('total_orders_cost') - Sum(F('order__order_payments__cost')), 0.)
        )

    def total_sum_count_aggragate(self):
        return self.aggregate(
            total_offers_count_sum=Sum('total_product_count'),
            total_clients_count_sum=Count('order__user_id', distinct=True),
            coupon_clients_count_sum=Count('order__user_id', distinct=True,
                                           filter=Q(coupon__isnull=False)),
            full_price_clients_count_sum=Count('order__user_id', distinct=True,
                                               filter=Q(coupon__isnull=True)),
            total_orders_count_sum=Sum('total_orders_count'),
            coupon_orders_count_sum=Sum('coupon_orders_count'),
            full_price_orders_count_sum=Sum('full_price_orders_count'),
            total_orders_cost_sum=Sum('total_orders_cost'),
            coupon_orders_cost_sum=Sum('coupon_orders_cost'),
            full_price_orders_cost_sum=Sum('full_price_orders_cost'),
        )


class StatisticsCategoryMixin:

    def sum_count_annotate(self):
        return self.annotate(
            total_clients_count=Count('user__id', distinct=True),
            coupon_clients_count=Count('user__id', distinct=True,
                                       filter=Q(user__order__producttoorder__coupon__isnull=False)),
            full_price_clients_count=Count('user__id', distinct=True,
                                           filter=Q(user__order__producttoorder__coupon__isnull=True)),
            total_orders_count=Count('user__order__id', distinct=True),
            coupon_orders_count=Count('user__order__id', distinct=True,
                                      filter=Q(user__order__producttoorder__coupon__isnull=False)),
            full_price_orders_count=Count('user__order__id', distinct=True,
                                          filter=Q(user__order__producttoorder__coupon__isnull=True)),
            total_orders_cost=Coalesce(
                Sum(F('user__order__producttoorder__qty') * F('user__order__producttoorder__cost')), 0.),
            coupon_orders_cost=Coalesce(
                Sum(F('user__order__producttoorder__qty') * F('user__order__producttoorder__cost'),
                    filter=Q(user__order__producttoorder__coupon__isnull=False)), 0.),
            full_price_orders_cost=Coalesce(
                Sum(F('user__order__producttoorder__qty') * F('user__order__producttoorder__cost'),
                    filter=Q(user__order__producttoorder__coupon__isnull=True)), 0.),
            last_order_date=Max('user__order__create_date__date'),
            debt=Coalesce(F('total_orders_cost') - Sum(F('user__order__order_payments__cost')), 0.),
        )

    def total_sum_count_aggragate(self):
        return self.aggregate(
            total_clients_count_sum=Count('user__id', distinct=True),
            coupon_clients_count_sum=Count('user__id', distinct=True,
                                           filter=Q(user__order__producttoorder__coupon__isnull=False)),
            full_price_clients_count_sum=Count('user__id', distinct=True,
                                               filter=Q(user__order__producttoorder__coupon__isnull=True)),
            total_orders_count_sum=Sum('total_orders_count'),
            coupon_orders_count_sum=Sum('coupon_orders_count'),
            full_price_orders_count_sum=Sum('full_price_orders_count'),
            total_orders_cost_sum=Sum('total_orders_cost'),
            coupon_orders_cost_sum=Sum('coupon_orders_cost'),
            full_price_orders_cost_sum=Sum('full_price_orders_cost'),
        )


class StatisticsUserMixin:

    def sum_count_annotate(self):
        return self.annotate(
            total_clients_count=Count('id', distinct=True),
            coupon_clients_count=Count('id', distinct=True, filter=Q(order__producttoorder__coupon__isnull=False)),
            full_price_clients_count=Count('id', distinct=True, filter=Q(order__producttoorder__coupon__isnull=True)),
            total_orders_count=Count('order__id', distinct=True),
            coupon_orders_count=Count('order__id', distinct=True,
                                      filter=Q(order__producttoorder__coupon__isnull=False)),
            # coupon=F('order__producttoorder__coupon'),
            full_price_orders_count=Count('order__id', distinct=True,
                                          filter=Q(order__producttoorder__coupon__isnull=True)),
            total_orders_cost=Coalesce(Sum(F('order__producttoorder__qty') * F('order__producttoorder__cost')), 0.),
            coupon_orders_cost=Coalesce(Sum(F('order__producttoorder__qty') * F('order__producttoorder__cost'),
                                            filter=Q(order__producttoorder__coupon__isnull=False)), 0.),
            full_price_orders_cost=Coalesce(Sum(F('order__producttoorder__qty') * F('order__producttoorder__cost'),
                                                filter=Q(order__producttoorder__coupon__isnull=True)), 0.),
            last_order_date=Max('order__create_date__date'),
            debt=Coalesce(F('total_orders_cost') - Sum(F('order__order_payments__cost')), 0.),
        )

    def total_sum_count_aggragate(self):
        return self.aggregate(
            total_clients_count_sum=Count('id', distinct=True),
            coupon_clients_count_sum=Count('id', distinct=True,
                                           filter=Q(order__producttoorder__coupon__isnull=False)),
            full_price_clients_count_sum=Count('id', distinct=True,
                                               filter=Q(order__producttoorder__coupon__isnull=True)),
            total_orders_count_sum=Sum('total_orders_count'),
            coupon_orders_count_sum=Sum('coupon_orders_count'),
            full_price_orders_count_sum=Sum('full_price_orders_count'),
            total_orders_cost_sum=Sum('total_orders_cost'),
            coupon_orders_cost_sum=Sum('coupon_orders_cost'),
            full_price_orders_cost_sum=Sum('full_price_orders_cost'),
            total_debt=Sum('debt')
        )


class StatisticsSpecialistMixin:
    def sum_count_annotate(self):
        return self.annotate(
            total_clients_count=Count('producttoorder__order__user__id', distinct=True),
            coupon_clients_count=Count('producttoorder__order__user__id', distinct=True,
                                       filter=Q(producttoorder__coupon__isnull=False)),
            full_price_clients_count=Count('producttoorder__order__user__id', distinct=True,
                                           filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_count=Count('producttoorder__order__id', distinct=True),
            coupon_orders_count=Count('producttoorder__order__id', distinct=True,
                                      filter=Q(producttoorder__coupon__isnull=False)),
            full_price_orders_count=Count('producttoorder__order__id', distinct=True,
                                          filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost')), 0.),
            coupon_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost'),
                                            filter=Q(producttoorder__coupon__isnull=False)), 0.),
            full_price_orders_cost=Coalesce(Sum(F('producttoorder__qty') * F('producttoorder__cost'),
                                                filter=Q(producttoorder__coupon__isnull=True)), 0.)
        )

    def total_sum_count_aggragate(self):
        return self.aggregate(
            total_clients_count_sum=Count('id', distinct=True),
            coupon_clients_count_sum=Count('id', distinct=True,
                                           filter=Q(producttoorder__coupon__isnull=False)),
            full_price_clients_count_sum=Count('id', distinct=True,
                                               filter=Q(producttoorder__coupon__isnull=True)),
            total_orders_count_sum=Sum('total_orders_count'),
            coupon_orders_count_sum=Sum('coupon_orders_count'),
            full_price_orders_count_sum=Sum('full_price_orders_count'),
            total_orders_cost_sum=Sum('total_orders_cost'),
            coupon_orders_cost_sum=Sum('coupon_orders_cost'),
            full_price_orders_cost_sum=Sum('full_price_orders_cost'),
        )
