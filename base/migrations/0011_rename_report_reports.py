# Generated by Django 4.0 on 2022-02-12 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_report'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='Reports',
        ),
    ]