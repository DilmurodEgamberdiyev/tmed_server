from django.conf import settings
from django.db.models import Model, ForeignKey, CharField, ImageField, \
    DateTimeField, BooleanField, IntegerField, CASCADE, SET_NULL

from shared.django.managers import get_manager

ORGS_STATUSES = [
    [-3, 'Fail on moderation'],
    [0, 'Base'],
    [3, 'On moderate'],
    [5, 'Verified'],
]


class AppsOrganization(Model):
    name = CharField(max_length=128)
    logo = ImageField(blank=True, null=True)
    creator = CharField(max_length=128)
    owner = CharField(max_length=128, null=True, default=None, help_text="Owner's username from UMS")
    slug_name = CharField(unique=True, max_length=128)
    inn = CharField(max_length=32)

    # status = IntegerField(choices=ORGS_STATUSES, default=0)

    class Meta:
        managed = False
        db_table = 'apps_organization'


class AppsSpecialistCatTranslate(Model):
    spec_cat = ForeignKey("AppsSpecialistsCat", CASCADE)
    name = CharField(max_length=200)
    lang = CharField(max_length=8, choices=settings.LANGUAGES)

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['spec_cat']

    class Meta:
        managed = False
        db_table = 'apps_specialistcattranslate'
        unique_together = ('spec_cat', 'lang')


class AppsSpecialistsCat(Model):
    """ Organizations' specialists' categories model. """

    org = ForeignKey("AppsOrganization", CASCADE)
    name = CharField(max_length=128)
    status = BooleanField(default=True)

    objects = get_manager('translate')
    TRANSLATE_FIELDS = ['name']

    TRANSLATE_MODEL = AppsSpecialistCatTranslate

    class Meta:
        managed = False
        db_table = 'apps_specialistscat'

    def __str__(self):
        return self.name


class AppsSpecialistBMS(Model):
    user = CharField(max_length=128)  # Foreign key to UMS.users
    name = CharField(max_length=128, blank=True)
    lastname = CharField(max_length=128, blank=True)
    spec_cat = ForeignKey(
        AppsSpecialistsCat, SET_NULL, null=True, related_name='specialists'
    )
    org = ForeignKey(AppsOrganization, CASCADE)
    status = IntegerField()

    class Meta:
        managed = False
        db_table = 'apps_specialist'


class AppsSpecialistTimeTracker(Model):
    start_time = DateTimeField(auto_now_add=True)
    end_time = DateTimeField(null=True)
    device = CharField(max_length=26, help_text='equipment_code from PMS')
    specialist = ForeignKey(AppsSpecialistBMS, CASCADE, related_name='time_trackers')
    is_overtime = BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'apps_specialisttimetracker'
