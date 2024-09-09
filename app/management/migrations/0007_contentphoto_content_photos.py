# Generated by Django 5.0.6 on 2024-09-09 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_photo_remove_content_tags_remove_aboutus_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.content', verbose_name='content')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.photo', verbose_name='photo')),
            ],
            options={
                'verbose_name': 'Content photo',
                'verbose_name_plural': 'Content photos',
                'db_table': 'content_photos',
                'unique_together': {('content', 'photo')},
            },
        ),
        migrations.AddField(
            model_name='content',
            name='photos',
            field=models.ManyToManyField(related_name='content_photos', through='management.ContentPhoto', to='management.photo', verbose_name='Photos'),
        ),
    ]