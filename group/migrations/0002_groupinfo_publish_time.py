# Generated by Django 4.1 on 2022-09-25 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="groupinfo",
            name="publish_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
