# Generated by Django 4.1.2 on 2022-10-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("time_log", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timelog",
            name="start_time",
            field=models.DateTimeField(),
        ),
    ]