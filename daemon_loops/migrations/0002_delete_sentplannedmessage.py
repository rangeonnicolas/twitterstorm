# Generated by Django 3.0.6 on 2020-11-22 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daemon_loops', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SentPlannedMessage',
        ),
    ]
