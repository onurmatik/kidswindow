# Generated by Django 3.1 on 2020-09-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_auto_20200902_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='type',
            field=models.CharField(choices=[('g', 'Game'), ('e', 'Event'), ('t', 'Tournament')], default='g', max_length=1, verbose_name='Meeting type'),
        ),
    ]
