from django.contrib import admin

from rooms.models import Room

from .models import Topic


class RoomsInline(admin.TabularInline):
    model = Room
    extra = 0
    readonly_fields = [
        "host",
        "name",
        "description",
        "participants",
    ]


class TopicAdmin(admin.ModelAdmin):
    inlines = [RoomsInline]


admin.site.register(Topic, TopicAdmin)
