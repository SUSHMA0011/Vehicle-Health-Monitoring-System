# Generated by Django 3.2.23 on 2024-06-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0037_delete_passwordrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25)),
                ('contact', models.CharField(max_length=10)),
            ],
        ),
    ]