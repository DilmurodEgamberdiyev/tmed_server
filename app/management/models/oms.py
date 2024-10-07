from django.db.models import Model, BigAutoField, CharField, BooleanField, IntegerField, ForeignKey, FloatField, \
    DateField, CASCADE, PROTECT, ManyToManyField, TextField, DO_NOTHING, SlugField, SET_NULL, SmallIntegerField

from management.models.ums import User
from shared.django.managers import get_manager


class AppsCurrency(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=128)
    code = CharField(unique=True, max_length=5)
    status = BooleanField()

    class Meta:
        managed = False
        db_table = 'apps_currency'


class AppsCategory(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=200)
    hide_from_orgs = BooleanField()
    hide_from_users = BooleanField()
    image = CharField(max_length=100, blank=True, null=True)
    status = BooleanField()
    description = TextField(blank=True, null=True)
    first_level_score = IntegerField()
    level_progress_by = IntegerField()
    parent = ForeignKey('self', DO_NOTHING, blank=True, null=True)

    objects = get_manager('translate', 'statistic_category')
    TRANSLATE_MODEL = 'AppsCategoryTranslate'
    TRANSLATE_FIELDS = ['name', 'description']

    class Meta:
        managed = False
        db_table = 'apps_category'


class AppsCategoryTranslate(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=200)
    description = TextField(blank=True, null=True)
    lang = CharField(max_length=8)
    category = ForeignKey(AppsCategory, DO_NOTHING, related_name='categories')

    class Meta:
        managed = False
        db_table = 'apps_categorytranslate'
        unique_together = (('category', 'lang'),)

class AppsRegionTranslate(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=256)
    lang = CharField(max_length=8)
    region = ForeignKey('AppsRegion', DO_NOTHING, related_name='regiontranslate')

    class Meta:
        managed = False
        db_table = 'apps_regiontranslate'
        unique_together = (('region', 'lang'),)


class AppsRegion(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=256)
    status = BooleanField()
    type = IntegerField(blank=True, null=True)
    parent = ForeignKey('self', DO_NOTHING, blank=True, null=True)

    objects = get_manager('translate', )
    TRANSLATE_FIELDS = ['name']
    TRANSLATE_MODEL = AppsRegionTranslate

    class Meta:
        managed = False
        db_table = 'apps_region'


class AppsUser(Model):
    username = SlugField(unique=True)
    name = CharField(max_length=128)
    lastname = CharField(max_length=128)
    main_cat = ForeignKey("AppsCategory", SET_NULL, null=True, blank=True, default=None,
                          related_name='user')
    avatar = CharField(max_length=1024, default=None, null=True, blank=True)

    gender = CharField(max_length=16, null=True, blank=True)
    birthday = DateField(blank=True, null=True)
    birthdate = DateField(blank=True, null=True)
    region = ForeignKey('AppsRegion', SET_NULL, null=True, blank=True)
    status = SmallIntegerField(default=0)
    pinfl = CharField(max_length=14, null=True, blank=True, default=None)

    objects = get_manager('translate', 'statistic_user')
    TRANSLATE_FIELDS = ['main_cat', 'region']

    class Meta:
        managed = False
        db_table = 'apps_user'

    # @property
    # def birthday(self):
    #     return self.user.birthday

    @property
    def user(self) -> User:
        return User.objects.using('ums').get(username=self.username)

    @property
    def full_name(self):
        return f"{self.lastname} {self.name}"


class AppsHashtagCategory(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=512)

    class Meta:
        managed = False
        db_table = 'apps_hashtagcategory'


class AppsHashtag(Model):
    id = BigAutoField(primary_key=True)
    code = CharField(max_length=20, blank=True, null=True)
    description = CharField(max_length=1024)
    category = ForeignKey('AppsHashtagCategory', DO_NOTHING)
    parent = ForeignKey('self', DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apps_hashtag'


class AppsSpecialistHashtag(Model):
    specialist = ForeignKey('AppsSpecialist', CASCADE)
    hashtag = ForeignKey('AppsHashtag', CASCADE)

    class Meta:
        unique_together = ['specialist', 'hashtag']
        managed = False
        db_table = 'apps_specialisthashtag'


class AppsSpecialist(Model):
    org = CharField(max_length=128, help_text='org slug from BMS')
    spec_cat = IntegerField(help_text='specialist category id from BMS')
    job = ForeignKey('AppsCategory', PROTECT)
    auto = BooleanField(default=True)
    name = CharField(max_length=128, default=None, null=True)
    lastname = CharField(max_length=128, default=None, null=True)
    avatar = CharField(max_length=1024, default=None, null=True)
    status = IntegerField(default=1)
    is_great = BooleanField(default=False)

    # image = CharField(max_length=1024, default=None, null=True)
    user = ForeignKey('AppsUser', PROTECT)

    hashtags = ManyToManyField(
        to='AppsHashtag', through='AppsSpecialistHashtag',
        related_name='specialists'
    )

    objects = get_manager('translate', 'statistic_specialist')
    TRANSLATE_FIELDS = ['job']

    class Meta:
        managed = False
        db_table = 'apps_specialist'


class AppsPlanHistory(Model):
    specialist = ForeignKey('AppsSpecialist', CASCADE)
    type = IntegerField()
    day = IntegerField()
    value = FloatField()
    date = DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'apps_planhistory'
