# Generated by Django 3.2.23 on 2024-06-20 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PROJECTApp', '0028_rename_old_password_user_new_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='new_password',
        ),
    ]