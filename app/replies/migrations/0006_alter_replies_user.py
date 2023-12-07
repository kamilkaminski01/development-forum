# Generated by Django 4.1.7 on 2023-12-07 20:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("replies", "0005_replies_accepted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="replies",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="replies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]