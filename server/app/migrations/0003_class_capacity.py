# Generated by Django 5.1 on 2025-05-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_classbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
