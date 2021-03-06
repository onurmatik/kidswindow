# Generated by Django 3.1 on 2020-09-02 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20200902_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='join_url',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='start_url',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='topic',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='slug',
            field=models.SlugField(blank=True, editable=False, null=True),
        ),
    ]
