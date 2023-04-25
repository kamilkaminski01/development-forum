from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UsersAdmin(UserAdmin):
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_superuser",
    ]
    readonly_fields = ["date_joined", "last_login"]

    add_fieldsets = (
        (
            "General",
            {
                "classes": ("wide",),
                "fields": [
                    "username",
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "fields": [
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "last_login",
                ],
            },
        ),
    )

    fieldsets = (
        (
            "General",
            {
                "classes": ("wide",),
                "fields": [
                    "username",
                    "email",
                    "password",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "fields": [
                    "is_staff",
                    "is_active",
                    "date_joined",
                    "last_login",
                ],
            },
        ),
    )


admin.site.register(User, UsersAdmin)
