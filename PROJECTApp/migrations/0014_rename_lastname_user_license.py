# Generated by Django 3.2.23 on 2024-05-31 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0013_remove_mileage_calculatedmileage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='lastname',
            new_name='license',
        ),
    ]
