# Generated by Django 3.1 on 2020-09-02 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_auto_20200829_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='slug',
            field=models.SlugField(default='*'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MeetingRequest',
        ),
    ]
