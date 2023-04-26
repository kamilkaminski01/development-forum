from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from rooms.models import Room
from topics.models import Topic
from users.models import User


class TestRoomDelete(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("delete-room", kwargs={"pk": 1})
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

    def test_delete_room(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Room.objects.get(id=1)
