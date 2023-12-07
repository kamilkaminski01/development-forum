from django.contrib import admin

from .models import Replies


class RepliesAdmin(admin.ModelAdmin):
    list_display = [
        "truncated_body",
        "accepted",
        "user",
        "room",
    ]

    def truncated_body(self, obj) -> str:
        return obj.body[:20] + "..." if len(obj.body) > 20 else obj.body


admin.site.register(Replies, RepliesAdmin)
