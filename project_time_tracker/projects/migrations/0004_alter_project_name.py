# Generated by Django 4.1.2 on 2022-10-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0003_alter_projectassignment_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(max_length=32, unique=True),
        ),
    ]