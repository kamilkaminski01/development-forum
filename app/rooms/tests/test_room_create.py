from django.test import Client, TestCase
from django.urls import reverse

from rooms.models import Room
from topics.models import Topic
from users.models import User


class TestRoomCreate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("create-room")
        self.user = User.objects.create(  # type: ignore
            email="test@user.com",
            username="test",
        )
        self.user.set_password("Test-123")
        self.user.save()

    def test_create_room(self):
        self.client.login(email=self.user.email, password="Test-123")
        data = {
            "name": "learning python",
            "topic": "python",
            "description": "testing long description",
        }
        response = self.client.post(self.url, data)
        room = Room.objects.first()
        topic = Topic.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(room.host, self.user)
        self.assertEqual(topic.name, "python")
        self.assertEqual(room.name, "learning python")
        self.assertEqual(room.description, "testing long description")

    def test_not_authenticated_create_room(self):
        data = {
            "name": "creating room not being logged in",
            "topic": "python",
            "description": "testing long description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(Room.objects.first())
