from typing import List

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .utils import validate_file_extension


def upload_to_avatars(instance, filename: str) -> str:
    return f"avatars/{instance.id}/{filename}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        if not password:
            raise TypeError("Superusers must have a password")
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=upload_to_avatars,
        validators=[validate_file_extension],
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()  # type: ignore
