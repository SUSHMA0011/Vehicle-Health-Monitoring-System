# Generated by Django 3.2.23 on 2024-05-30 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0011_auto_20240530_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='mileage',
            name='calculatedMileage',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
