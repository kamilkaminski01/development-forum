from pathlib import Path

from django.core.exceptions import ValidationError


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def validate_file_extension(value):
    extension = get_file_extension(value.name)
    valid_extensions = [".png", ".jpg", ".jpeg", ".svg", ".webp"]
    if extension not in valid_extensions:
        raise ValidationError("File not supported")
