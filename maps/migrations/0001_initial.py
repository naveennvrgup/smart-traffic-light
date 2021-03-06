# Generated by Django 3.1.1 on 2020-09-22 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrafficSignal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('long', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='TrafficLight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.IntegerField()),
                ('signal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.trafficsignal')),
            ],
        ),
    ]
