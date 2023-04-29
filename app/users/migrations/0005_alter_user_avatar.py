# Generated by Django 4.1.7 on 2023-04-29 13:19

from django.db import migrations, models

import users.models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=users.models.upload_to_avatars,
                validators=[users.utils.validate_file_extension],
            ),
        ),
    ]
