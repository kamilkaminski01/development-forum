# Generated by Django 4.1.7 on 2023-04-18 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_topic_room_host_room_topic_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="topic",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.SET_NULL, to="base.topic"
            ),
        ),
    ]