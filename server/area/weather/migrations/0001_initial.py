# Generated by Django 4.1.2 on 2023-01-28 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('feels_like', models.FloatField()),
                ('temp_min', models.FloatField()),
                ('temp_max', models.FloatField()),
                ('pressure', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_deg', models.FloatField()),
                ('clouds_all', models.FloatField()),
                ('weather_id', models.FloatField()),
                ('weather_main', models.CharField(max_length=100)),
                ('weather_description', models.CharField(max_length=100)),
                ('weather_icon', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
