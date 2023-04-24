from django.contrib.auth.models import User
from django.db import models

from topics.models import Topic


class Room(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="room_host"
    )
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return str(self.name)
