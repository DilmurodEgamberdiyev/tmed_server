from django.db.models import CharField, BooleanField, ForeignKey, DateField, TextField, DO_NOTHING, SlugField, \
    SmallIntegerField, PositiveBigIntegerField, EmailField, IntegerField, CASCADE, PositiveIntegerField
from django.db.models import Model, TextChoices

USER_STATUSES = [
    [-1, 'Banned'],
    [1, 'Profile filled'],
    [2, 'Verified'],
]

PERMISSION_LEVEL = (
    (1, 'admin'),
    (2, 'organization')
)


class UMSSpecialist(Model):
    org = CharField(max_length=128, help_text='org slug from BMS')
    spec_cat = IntegerField(help_text='specialist category id from BMS')
    auto = BooleanField(default=True)
    name = CharField(max_length=128, default=None, null=True)
    lastname = CharField(max_length=128, default=None, null=True)
    avatar = CharField(max_length=1024, default=None, null=True)
    username = CharField(max_length=128)
    job = IntegerField()

    class Meta:
        managed = False
        db_table = 'apps_specialist'


class UMSCategoryTranslate(Model):
    """ Translate model of users and organizations categories. """

    category = ForeignKey("UMSCategory", CASCADE, related_name='categories')
    name = CharField(max_length=200)
    description = TextField(blank=True, null=True)
    lang = CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'apps_categorytranslate'


class UMSCategory(Model):
    name = CharField(max_length=200)
    parent = ForeignKey('self', on_delete=CASCADE, blank=True, null=True)
    hide_from_orgs = BooleanField(default=True)
    hide_from_users = BooleanField(default=False)
    # image = ImagePathField(max_length=255, blank=True, null=True)
    status = BooleanField(default=True)
    description = TextField(blank=True, null=True)
    first_level_score = PositiveIntegerField(default=5)
    level_progress_by = PositiveIntegerField(default=3)
    creator = CharField(max_length=128, null=True, default=None, help_text='username from UMS')

    class Meta:
        managed = False
        db_table = 'apps_category'


class User(Model):
    class Type(TextChoices):
        USER = 'user', 'User'
        COMPANY = 'company', 'Company'

    username = SlugField(max_length=150, unique=True, allow_unicode=False)
    password = CharField(max_length=150)
    email = EmailField(blank=True, null=True)
    phone = CharField(max_length=255, unique=True, blank=True, null=True,
                      default=None)
    name = CharField(max_length=150)
    lastname = CharField(max_length=150, blank=True, null=True)
    surname = CharField(max_length=150, blank=True, null=True)
    gender = CharField(max_length=16, blank=True, null=True)
    birthday = DateField(blank=True, null=True)
    bio = TextField(blank=True, null=True)
    is_official = BooleanField(default=0)
    status = SmallIntegerField(choices=USER_STATUSES, default=0)
    phone_activated = BooleanField(default=True)
    enable_send_pvc = BooleanField(default=False)
    is_related = BooleanField(default=False)
    pvc = CharField(max_length=150, null=True, blank=True)
    region_id = PositiveBigIntegerField(null=True, blank=True)
    experience = CharField(max_length=128, null=True, blank=True, default=None)
    education = CharField(max_length=6, null=True, blank=True, default=None)
    main_cat = ForeignKey(UMSCategory, DO_NOTHING, null=True, blank=True, default=None)
    nationality = CharField(max_length=255, null=True, blank=True)
    current_place = CharField(max_length=255, null=True, blank=True, default=None)
    is_afgan = BooleanField(default=False)
    is_cherno = BooleanField(default=False)
    is_invalid = BooleanField(default=False)
    is_uvu = BooleanField(default=False)
    position = CharField(max_length=255, null=True, blank=True)
    type = CharField(max_length=255, choices=Type.choices, default=Type.USER)
    owner = CharField(max_length=255, choices=Type.choices, default=Type.USER)

    specialist = ForeignKey(UMSSpecialist, DO_NOTHING, null=True, default=None)

    pinfl = CharField(max_length=14, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'apps_user'
