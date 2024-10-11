from django.db.models import TextField, CharField, EmailField, ImageField, TextChoices, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from shared.django import TimeAndOrderBaseModel


class Management(TimeAndOrderBaseModel):
    """
    This model represents the management or leadership profiles.

    Attributes:
        file (ImageField): The profile image of the management person.
        phone_number (CharField): The contact phone number.
        email (EmailField): The contact email address.
        administration_type (CharField): The type of administration (e.g., Administration, Leadership).
        full_name (CharField): The full name of the person. # t
        role (CharField): The role or position of the person. # t
        reception_day (CharField): The reception day for public visits. # t
        job_description (TextField): The job description of the person. # t
        permission (TextField): The permissions or authority held by the person. # t
    """

    class ManagementTypeChoices(TextChoices):
        """
        An enumeration for different types of management.
        """
        ADMINISTRATION = 'ADMINISTRATION', _('Administration')
        LEADERSHIP = 'LEADERSHIP', _('Leadership')

    file = ImageField(
        upload_to='administration/',
        verbose_name=_('Profile Image'),
        help_text=_('Upload the profile image of the person.')
    )
    phone_number = CharField(
        max_length=20,
        verbose_name=_('Phone Number'),
        help_text=_('Enter the contact phone number.'),
        # e.g., '+998712445533'
    )
    email = EmailField(
        verbose_name=_('Email'),
        help_text=_('Enter the contact email address.'),
        # e.g., 'example@example.com'
    )
    administration_type = CharField(
        max_length=20,
        choices=ManagementTypeChoices.choices,
        verbose_name=_('Administration Type'),
        help_text=_('Select the type of administration.'),
        # e.g., 'Administration', 'Leadership'
    )
    full_name = CharField(
        max_length=255,
        verbose_name=_('Full Name'),
        help_text=_('Enter the full name of the person.'),
        # e.g., 'John Doe'
    )
    role = CharField(
        max_length=255,
        verbose_name=_('Role'),
        help_text=_('Enter the role or position of the person.'),
        # e.g., 'Chief Executive Officer'
    )
    reception_day = CharField(
        max_length=255,
        verbose_name=_('Reception Day'),
        help_text=_('Enter the reception day for public visits.'),
        # e.g., 'Monday to Friday'
    )
    job_description = TextField(
        verbose_name=_('Job Description'),
        help_text=_('Provide a detailed job description of the person.'),
        # e.g., 'Responsible for overseeing all operations.'
    )
    permission = TextField(
        verbose_name=_('Permission'),
        help_text=_('Specify the permissions or authority held by the person.'),
        # e.g., 'Can approve major decisions.'
    )

    class Meta:
        ordering = '-order',
        db_table = 'management'
        verbose_name = _('Management')
        verbose_name_plural = _('Managements')

    def __str__(self):
        return self.full_name


class ContentPhoto(TimeAndOrderBaseModel):
    content = ForeignKey('management.Content', CASCADE, 'photos', verbose_name=_('content'))
    photo = ImageField(_('photo'), upload_to='contents/photos/main/')

    class Meta:
        ordering = '-order',
        unique_together = 'content', 'photo'
        db_table = 'content_photos'
        verbose_name = _('Content photo')
        verbose_name_plural = _('Content photos')

    def __str__(self):
        return self.photo.url


class Content(TimeAndOrderBaseModel):
    class ContentType(TextChoices):
        NEWS = 'NEWS', _('News')
        KNOWLEDGE = 'KNOWLEDGE', _('Knowledge')
        POST = 'POST', _('Post')

    title = CharField(max_length=255, verbose_name=_('Title'))
    content = CKEditor5Field(
        verbose_name=_('Content'),
        help_text=_('Provide a detailed description about the content.'),
        config_name='extends'
    )
    type = CharField(choices=ContentType.choices, verbose_name=_('Type'))
    main_photo = ImageField(verbose_name=_('Main main_photo'), upload_to='contents/photos/main')

    class Meta:
        ordering = '-order',
        db_table = 'content'
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')
        unique_together = 'type', 'title'

    def __str__(self):
        return self.title
