# Generated by Django 3.0.6 on 2020-11-22 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SentPlannedMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campain_id', models.CharField(max_length=50)),
                ('planned_message_id', models.CharField(max_length=50)),
                ('sent_at', models.DateField()),
                ('sender_id', models.CharField(max_length=50)),
                ('sent_text', models.TextField()),
            ],
        ),
    ]
