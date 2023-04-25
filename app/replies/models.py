from django.db import models

from rooms.models import Room
from users.models import User


class Replies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="replies")
    body = models.TextField(max_length=150)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:50]
