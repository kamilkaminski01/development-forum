from django.contrib import admin

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "topic",
        "host",
    ]


admin.site.register(Room, RoomAdmin)
