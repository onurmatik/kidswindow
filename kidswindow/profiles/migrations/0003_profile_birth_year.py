# Generated by Django 3.1 on 2020-09-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_profile_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_year',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]