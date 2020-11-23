# Generated by Django 3.0.6 on 2020-11-23 02:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('daemon_loops', '0005_auto_20201122_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostedTweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campain_id', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=300)),
                ('date_received', models.DateTimeField()),
                ('sender_id', models.CharField(max_length=50)),
            ],
        ),
    ]