# Generated by Django 3.1.1 on 2020-10-22 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0013_auto_20201022_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafficlight',
            name='heartbeat',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 22, 15, 33, 1, 263411)),
        ),
        migrations.AlterField(
            model_name='trafficsignal',
            name='timer',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 22, 15, 33, 1, 230443)),
        ),
    ]