# Generated by Django 3.2.23 on 2024-06-18 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0025_tyre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
