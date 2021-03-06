# Generated by Django 3.1 on 2020-08-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meeting',
            options={'verbose_name': 'meeting', 'verbose_name_plural': 'meetings'},
        ),
        migrations.AlterModelOptions(
            name='meetingparticipant',
            options={'verbose_name': 'meeting participant', 'verbose_name_plural': 'meeting participants'},
        ),
        migrations.AlterModelOptions(
            name='meetingpoll',
            options={'verbose_name': 'meeting poll', 'verbose_name_plural': 'meeting polls'},
        ),
        migrations.AlterModelOptions(
            name='meetingrequest',
            options={'verbose_name': 'meeting request', 'verbose_name_plural': 'meeting requests'},
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='type',
        ),
        migrations.AddField(
            model_name='meeting',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
