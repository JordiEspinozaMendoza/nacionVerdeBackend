# Generated by Django 4.0 on 2022-02-12 17:53

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_rename_report_reports'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
