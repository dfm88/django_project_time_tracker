# Generated by Django 4.1.2 on 2022-10-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "time_log",
            "0003_timelog_end time (when not null) must be grater than start time",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="timelog",
            name="end_time",
            field=models.DateTimeField(db_index=True, default=None),
        ),
        migrations.AlterField(
            model_name="timelog",
            name="start_time",
            field=models.DateTimeField(db_index=True),
        ),
    ]
