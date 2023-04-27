from django.test import Client, TestCase
from django.urls import reverse

from rooms.models import Room
from topics.models import Topic
from users.models import User


class TestReplyCreate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client1 = Client()
        self.client2 = Client()
        self.url = reverse("room", kwargs={"pk": 1})
        self.user1, self.user2 = User.objects.bulk_create(  # type: ignore
            [
                User(
                    email="test1@user.com",
                    username="test1",
                ),
                User(
                    email="test2@user.com",
                    username="test2",
                ),
            ]
        )
        self.user1.set_password("Test-123")
        self.user2.set_password("Test-123")
        self.user1.save()
        self.user2.save()
        self.client1.login(email=self.user1.email, password="Test-123")
        self.client2.login(email=self.user2.email, password="Test-123")
        self.topic = Topic.objects.create(name="test topic")
        self.room = Room.objects.create(
            host=self.user1,
            name="test room",
            topic=self.topic,
            description="test description",
        )

    def test_create_reply(self):
        first_user_reply_data = {
            "user": self.user1,
            "room": self.room,
            "body": "sending first message",
            "updated": "2023-04-19T09:04:48.874Z",
            "created": "2023-04-19T07:02:16.874Z",
        }
        second_user_reply_data = {
            "user": self.user2,
            "room": self.room,
            "body": "sending second message",
            "updated": "2023-04-19T09:05:48.874Z",
            "created": "2023-04-19T07:03:16.874Z",
        }
        response1 = self.client1.post(self.url, first_user_reply_data)
        response2 = self.client2.post(self.url, second_user_reply_data)
        self.room.refresh_from_db()
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(self.room.participants.count(), 2)
        self.assertEqual(self.room.replies.count(), 2)
        self.assertEqual(self.room.participants.first(), self.user1)
        self.assertEqual(self.room.replies.first().body, second_user_reply_data["body"])
