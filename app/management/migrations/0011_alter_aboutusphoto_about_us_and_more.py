# Generated by Django 5.0.6 on 2024-09-09 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_remove_content_photos_remove_aboutus_photos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutusphoto',
            name='about_us',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='management.aboutus', verbose_name='About Us'),
        ),
        migrations.AlterField(
            model_name='contentphoto',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='management.content', verbose_name='content'),
        ),
    ]