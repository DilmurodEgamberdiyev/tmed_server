from hashlib import shake_256
from pathlib import Path

from django.db.models import Model, BigAutoField, BigIntegerField, ForeignKey, DO_NOTHING, CharField, ImageField, \
    DateTimeField, FloatField, BooleanField, ManyToManyField, TextChoices, IntegerField, TextField, CASCADE, \
    SmallIntegerField

from shared.django.managers import get_manager

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('ru', 'Russsian'),
    ('uz', 'Uzbek')
]


class UploadPath:

    def __init__(self, field_name, file_name_from='pk', hashing=True):
        self.field_name = field_name
        self.file_name_from = file_name_from
        self.hashing = hashing
        super(UploadPath, self).__init__()

    def __call__(self, instance, filename):
        ext = Path(filename).suffix
        filename = str(getattr(instance, self.file_name_from))
        if self.hashing:
            filename = shake_256(filename.encode()).hexdigest(5)
        filename = f'{filename}{ext}'
        return str(Path(instance.__class__.__name__, self.field_name, filename))

    def deconstruct(self):
        return f'{self.__module__}.{self.__class__.__name__}', [self.field_name], {}


class AppsGroup(Model):
    id = BigAutoField(primary_key=True)
    org = CharField(max_length=128)
    name = CharField(max_length=128)
    image = ImageField(upload_to=UploadPath('group'), null=True, default=None)
    create_date = DateTimeField(auto_now_add=True, null=True)
    vat = FloatField(default=12.0)
    discount = FloatField(default=0)
    cashback = FloatField(default=0)
    cancel_fine = FloatField(default=0)
    is_active = BooleanField(default=True)
    products = ManyToManyField(to='AppsProductToOrganization', through='AppsProductToGroup')

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['name']
    TRANSLATE_MODEL = "AppsGrouptranslate"

    class Meta:
        managed = False
        db_table = 'apps_group'
        unique_together = (('org', 'name'),)


class AppsProductToGroup(Model):
    id = BigAutoField(primary_key=True)
    group = ForeignKey(AppsGroup, DO_NOTHING)
    product = ForeignKey('AppsProductToOrganization', DO_NOTHING, related_name='product_to_group')

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['group']

    class Meta:
        managed = False
        db_table = 'apps_producttogroup'
        unique_together = (('product', 'group'),)


class AppsProductToOrganization(Model):
    class CashBackType(TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        SOM = 'som', 'Som'

    id = BigAutoField(primary_key=True)
    org = CharField(max_length=128)
    status = IntegerField()
    remains = IntegerField(blank=True, null=True)
    create_date = DateTimeField()
    update_date = DateTimeField()
    cashback = IntegerField(blank=True, null=True)
    cashback_type = CharField(max_length=255, choices=CashBackType.choices, default=CashBackType.PERCENTAGE)
    cancel_fine = IntegerField(blank=True, null=True)
    rec_cashback = IntegerField(blank=True, null=True)
    expire_date = DateTimeField(null=True, default=None)
    delay_cancel_fine = IntegerField(blank=True, null=True)
    vat = IntegerField(blank=True, null=True)
    is_official = BooleanField()
    dependence_sell = IntegerField()
    duration = IntegerField(blank=True, null=True)
    product = ForeignKey('AppsProduct', DO_NOTHING, to_field='code')
    groups = ManyToManyField(AppsGroup, through='AppsProductToGroup', related_name='org_products')
    surcharges = ManyToManyField('AppsSurcharge',
                                 through='AppsSurchargesInProductToOrganization',
                                 related_name='org_products')

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['product_to_group']

    class Meta:
        managed = False
        db_table = 'apps_producttoorganization'


class AppsManufacturer(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=256)
    org = CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apps_manufacturer'


class AppProductCategoryTranslate(Model):
    category = ForeignKey("AppsProductCategory", CASCADE, related_name='category_translates')
    name = CharField(max_length=256)
    lang = CharField(max_length=8, choices=LANGUAGE_CHOICES)

    LOOKUP_FIELD = 'category'

    class Meta:
        managed = False
        db_table = 'apps_categorytranslate'


class AppsProductCategory(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=200)
    parent = ForeignKey('self', CASCADE, blank=True, null=True)
    image = CharField(max_length=255, blank=True, null=True)
    status = IntegerField(default=1)

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['name']
    TRANSLATE_MODEL = AppProductCategoryTranslate

    class Meta:
        managed = False
        db_table = 'apps_category'


class AppsProductStatus(Model):
    id = BigAutoField(primary_key=True)
    value = SmallIntegerField()
    name = CharField(max_length=128)
    slug = CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'apps_productstatus'


class AppsUnitProductTranslate(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=32)
    lang = CharField(max_length=8)
    unit = ForeignKey('AppsUnitProduct', DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'apps_unitproducttranslate'
        unique_together = (('lang', 'unit'),)


class AppsUnitProduct(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=32)

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['name']
    TRANSLATE_MODEL = AppsUnitProductTranslate

    class Meta:
        managed = False
        db_table = 'apps_unitproduct'


class AppsProductType(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=256)

    class Meta:
        managed = False
        db_table = 'apps_producttype'


class AppsProductTranslate(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=512)
    description = TextField()
    lang = CharField(max_length=8)
    product = ForeignKey('AppsProduct', DO_NOTHING, related_name='product_translates')

    class Meta:
        managed = False
        db_table = 'apps_producttranslate'
        unique_together = (('product', 'lang'),)


class AppsProduct(Model):
    id = BigAutoField(primary_key=True)
    code = CharField(unique=True, max_length=32)
    name = CharField(max_length=512)
    description = TextField(blank=True, null=True)
    create_date = DateTimeField()
    update_date = DateTimeField()
    bar_code = CharField(max_length=20, blank=True, null=True)
    is_sell = BooleanField()
    category = ForeignKey("AppsProductCategory", CASCADE)
    manufacturer = ForeignKey('AppsManufacturer', DO_NOTHING)
    status = ForeignKey('AppsProductStatus', DO_NOTHING)
    type = ForeignKey('AppsProductType', DO_NOTHING)
    unit = ForeignKey('AppsUnitProduct', DO_NOTHING, blank=True, null=True)
    measure = FloatField(default=0)

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['name', 'unit']
    TRANSLATE_MODEL = AppsProductTranslate

    class Meta:
        managed = False
        db_table = 'apps_product'

    @property
    def get_price_uzs(self, ):
        # default currency uzs
        product_to_org = self.appsproducttoorganization_set.first()
        if product_to_org:
            product_price = product_to_org.appsproductprice_set.filter(currency_id='uzs').first()
            if product_price:
                return product_price.value


class AppsProductPrice(Model):
    id = BigAutoField(primary_key=True)
    value = FloatField()
    discount = IntegerField()
    active = BooleanField()
    create_date = DateTimeField()
    update_date = DateTimeField()
    max_qty = IntegerField(blank=True, null=True)
    min_qty = IntegerField(blank=True, null=True)
    currency = ForeignKey("AppsCurrency", DO_NOTHING, to_field='code')
    org_product = ForeignKey('AppsProductToOrganization', DO_NOTHING)
    is_wholesale = BooleanField()

    class Meta:
        managed = False
        db_table = 'apps_productprice'


class AppsSurcharge(Model):
    id = BigAutoField(primary_key=True)
    org = CharField(max_length=255)
    desc = CharField(max_length=255, blank=True, null=True)
    type = IntegerField()
    value = FloatField()
    is_active = BooleanField()
    currency = ForeignKey('management.AppsCurrency', DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'apps_surcharge'


class AppsSurchargesInProductToOrganization(Model):
    id = BigAutoField(primary_key=True)
    product = ForeignKey(AppsProductToOrganization, DO_NOTHING)
    surcharge = ForeignKey(AppsSurcharge, DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'apps_surchargesinproducttoorganization'


class AppsProductToSpecialist(Model):
    id = BigAutoField(primary_key=True)
    specialist = BigIntegerField()
    product = ForeignKey(AppsProductToOrganization, DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'apps_producttospecialist'
        unique_together = (('specialist', 'product'),)
