# Generated by Django 4.1.7 on 2023-04-24 21:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="host",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="room_host",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
