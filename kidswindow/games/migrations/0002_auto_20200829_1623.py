# Generated by Django 3.1 on 2020-08-29 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('name',), 'verbose_name': 'game', 'verbose_name_plural': 'games'},
        ),
    ]
