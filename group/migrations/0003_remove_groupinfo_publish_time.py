# Generated by Django 4.1 on 2022-09-25 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0002_groupinfo_publish_time"),
    ]

    operations = [
        migrations.RemoveField(model_name="groupinfo", name="publish_time",),
    ]
