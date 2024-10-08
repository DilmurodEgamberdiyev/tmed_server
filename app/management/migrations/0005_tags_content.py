# Generated by Django 5.0.6 on 2024-09-07 08:23

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_aboutus_description_en_aboutus_description_ru_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=255, null=True, unique=True, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=255, null=True, unique=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, null=True, unique=True, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Tags',
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Title')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(help_text='Provide a detailed description about the content.', verbose_name='Content')),
                ('content_ru', django_ckeditor_5.fields.CKEditor5Field(help_text='Provide a detailed description about the content.', null=True, verbose_name='Content')),
                ('content_uz', django_ckeditor_5.fields.CKEditor5Field(help_text='Provide a detailed description about the content.', null=True, verbose_name='Content')),
                ('content_en', django_ckeditor_5.fields.CKEditor5Field(help_text='Provide a detailed description about the content.', null=True, verbose_name='Content')),
                ('type', models.CharField(choices=[('NEWS', 'News'), ('KNOWLEDGE', 'Knowledge'), ('POST', 'Post')], verbose_name='Type')),
                ('main_photo', models.ImageField(upload_to='main_photos/', verbose_name='Main photo')),
                ('tags', models.ManyToManyField(to='management.tags')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
                'db_table': 'posts',
                'unique_together': {('type', 'title')},
            },
        ),
    ]
