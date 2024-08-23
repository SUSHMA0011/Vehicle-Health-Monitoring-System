# Generated by Django 3.2.23 on 2024-07-03 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0042_delete_fuel'),
    ]

    operations = [
        migrations.CreateModel(
            name='fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vnumber', models.CharField(max_length=10)),
                ('driverName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('billNumber', models.CharField(max_length=100)),
                ('fuelStation', models.CharField(max_length=100)),
                ('liter', models.FloatField()),
                ('amount', models.FloatField()),
                ('readings', models.FloatField()),
                ('fuelimage', models.ImageField(blank=True, null=True, upload_to='fuelimage/')),
            ],
        ),
    ]
