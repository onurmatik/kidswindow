# Generated by Django 3.1 on 2020-09-02 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20200902_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='cancellation_reason',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='cancelled',
        ),
    ]
