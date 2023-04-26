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
        self.client.login(email=self.user.email, password="Test-123")

    def test_create_room(self):
        data = {
            "name": "learning python",
            "topic": "python",
            "description": "testing long description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Room.objects.first().host, self.user)
        self.assertEqual(Topic.objects.first().name, "python")
        self.assertEqual(Room.objects.first().name, "learning python")
        self.assertEqual(Room.objects.first().description, "testing long description")
