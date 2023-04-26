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
            email="test@user.com",
            username="test",
        )
        self.user.set_password("Test-123")
        self.user.save()
        self.client.login(email=self.user.email, password="Test-123")
        self.topic = Topic.objects.create(name="test topic")
        self.room = Room.objects.create(
            host=self.user,
            name="test room",
            topic=self.topic,
            description="test description",
        )

    def test_update_room(self):
        updated_data = {
            "name": "test room updated",
            "topic": self.topic.name,
            "description": "test description updated",
        }
        response = self.client.post(self.url, updated_data)
        room = Room.objects.get(id=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(room.name, updated_data["name"])
        self.assertEqual(room.topic.name, updated_data["topic"])
        self.assertEqual(room.description, updated_data["description"])
