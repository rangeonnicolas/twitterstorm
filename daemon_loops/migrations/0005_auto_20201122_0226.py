# Generated by Django 3.0.6 on 2020-11-22 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daemon_loops', '0004_auto_20201122_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentplannedmessage',
            name='sent_at',
            field=models.DateTimeField(),
        ),
    ]
