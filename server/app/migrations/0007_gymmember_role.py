# Generated by Django 5.1 on 2025-05-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_classbooking_class_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymmember',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('admin', 'Admin')], max_length=5, null=True),
        ),
    ]
