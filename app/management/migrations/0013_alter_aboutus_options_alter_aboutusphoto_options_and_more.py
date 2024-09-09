# Generated by Django 5.0.6 on 2024-09-09 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_aboutus_order_aboutusphoto_order_content_order_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutus',
            options={'ordering': ('order',), 'verbose_name': 'About Us', 'verbose_name_plural': 'About Us'},
        ),
        migrations.AlterModelOptions(
            name='aboutusphoto',
            options={'ordering': ('order',), 'verbose_name': 'About Us Photo', 'verbose_name_plural': 'About Us Photos'},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ('order',), 'verbose_name': 'Content', 'verbose_name_plural': 'Contents'},
        ),
        migrations.AlterModelOptions(
            name='contentphoto',
            options={'ordering': ('order',), 'verbose_name': 'Content photo', 'verbose_name_plural': 'Content photos'},
        ),
        migrations.AlterModelOptions(
            name='law',
            options={'ordering': ('order',), 'verbose_name': 'Legislative Base', 'verbose_name_plural': 'Legislative Bases'},
        ),
        migrations.AlterModelOptions(
            name='management',
            options={'ordering': ('order',), 'verbose_name': 'Management', 'verbose_name_plural': 'Managements'},
        ),
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ('order',), 'verbose_name': 'Structure', 'verbose_name_plural': 'Structures'},
        ),
    ]
