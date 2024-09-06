from django.db.models import ImageField, FileField, CharField, URLField, TextChoices
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from shared.django import TimeBaseModel


class AboutUs(TimeBaseModel):
    """
    This model represents the 'About Us' section of the website.
    It includes a descriptive text and an image.

    Attributes:
        description (CKEditor5Field): The descriptive text for the 'About Us' section.
        photo (ImageField): The image associated with the 'About Us' section.
    """

    description = CKEditor5Field(
        verbose_name=_('Description'),
        help_text=_('Provide a detailed description about the organization.'),
        config_name='extends'
    )
    photo = ImageField(
        upload_to='about_us/',
        verbose_name=_('Photo'),
        help_text=_('Upload an image representing the organization.')
    )

    class Meta:
        db_table = 'about_us'
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')

    def __str__(self):
        return _('About Us section').__str__()


class Structure(TimeBaseModel):
    """
    This model stores the organizational structure images.

    Attributes:
        image (ImageField): The image representing the structure.
    """

    image = ImageField(
        upload_to='structure/',
        verbose_name=_('Structure Image'),
        help_text=_('Upload an image representing the structure of the organization.')
    )

    class Meta:
        db_table = 'structure'
        verbose_name = _('Structure')
        verbose_name_plural = _('Structures')

    def __str__(self):
        return self.image.url


class Law(TimeBaseModel):
    """
    This model stores various laws, including their files and links.

    Attributes:
        file (FileField): The file associated with the law.
        name (CharField): The name of the law. # t
        law_type (CharField): The type of the law (e.g., LAW, PRESIDENTIAL, etc.).
        link (URLField): The link to the law document or webpage.
    """

    class LawChoices(TextChoices):
        """
        An enumeration for different types of laws.
        """
        LAW = 'LAW', _('Law')
        PRESIDENTIAL = 'PRESIDENTIAL', _('Presidential')
        CABINET = 'CABINET', _('Cabinet')
        RAILWAY = 'RAILWAY', _('Railway')
        SSV = 'SSV', _('SSV')

    file = FileField(
        upload_to='laws/',
        verbose_name=_('File'),
        help_text=_('Upload the law document file.')
    )
    name = CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Enter the name of the law.'),
        # e.g., 'Constitutional Law on Human Rights'
    )
    law_type = CharField(
        max_length=20,
        choices=LawChoices.choices,
        verbose_name=_('Law Type'),
        help_text=_('Select the type of the law.'),
        # e.g., 'LAW', 'PRESIDENTIAL'
    )
    link = URLField(
        verbose_name=_('Link'),
        help_text=_('Provide a link to the law document or webpage.')
    )

    class Meta:
        db_table = 'law'
        verbose_name = _('Legislative Base')
        verbose_name_plural = _('Legislative Bases')

    def __str__(self):
        return self.name
