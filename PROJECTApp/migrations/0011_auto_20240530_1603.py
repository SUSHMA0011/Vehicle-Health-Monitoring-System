# Generated by Django 3.2.23 on 2024-05-30 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0010_auto_20240530_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mileage',
            old_name='last_filled_kilometer',
            new_name='lastFilledKilometer',
        ),
        migrations.RenameField(
            model_name='mileage',
            old_name='number_of_liter',
            new_name='numberOfLiter',
        ),
        migrations.RenameField(
            model_name='mileage',
            old_name='present_kilometer',
            new_name='presentKilometer',
        ),
    ]
