# Generated by Django 3.1.1 on 2020-10-22 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0012_auto_20201019_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='trafficlight',
            name='heartbeat',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 22, 11, 20, 52, 487843)),
        ),
        migrations.AlterField(
            model_name='trafficsignal',
            name='timer',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 22, 11, 20, 52, 463673)),
        ),
    ]
