from django.test import Client, TestCase
from django.urls import reverse

from rooms.models import Room
from topics.models import Topic
from users.models import User


class TestRoomUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("update-room", kwargs={"pk": 1})
        self.user = User.objects.create(  # type: ignore
            email="user@user.com",
            username="user",
        )
        self.moderator = User.objects.create(  # type: ignore
            email="moderator@moderator.com",
            username="moderator",
            is_staff=True,
        )
        self.user.set_password("Test-123")
        self.moderator.set_password("Test-123")
        self.user.save()
        self.moderator.save()
        self.topic = Topic.objects.create(name="test topic")
        self.room = Room.objects.create(
            host=self.user,
            name="test room",
            topic=self.topic,
            description="test description",
        )

    def test_update_room(self):
        self.client.login(email=self.user.email, password="Test-123")
        updated_data = {
            "name": "test room updated",
            "topic": self.topic.name,
            "description": "test description updated",
        }
        response = self.client.post(self.url, updated_data)
        self.room.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.room.name, updated_data["name"])
        self.assertEqual(self.room.topic.name, updated_data["topic"])
        self.assertEqual(self.room.description, updated_data["description"])

    def test_staff_update_room(self):
        self.client.login(email=self.moderator.email, password="Test-123")
        updated_data = {
            "name": "test room updated",
            "topic": self.topic.name,
            "description": "test description updated",
        }
        response = self.client.post(self.url, updated_data)
        self.room.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.room.name, updated_data["name"])
        self.assertEqual(self.room.topic.name, updated_data["topic"])
        self.assertEqual(self.room.description, updated_data["description"])
