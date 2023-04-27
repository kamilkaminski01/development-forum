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

    def test_delete_room(self):
        self.client.login(email=self.user.email, password="Test-123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Room.objects.get(id=1)

    def test_staff_delete_room(self):
        self.client.login(email=self.moderator.email, password="Test-123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Room.objects.get(id=1)

    def test_user_not_authenticated_delete_room(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(self.room)
