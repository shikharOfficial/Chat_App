# Generated by Django 5.0.4 on 2024-04-24 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_tbluser_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbluser',
            name='last_login',
        ),
    ]