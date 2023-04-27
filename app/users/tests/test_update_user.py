from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class TestUpdateUser(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("update-user", kwargs={"pk": 1})
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

    def test_update_user(self):
        self.client.login(email=self.user.email, password="Test-123")
        updated_user_data = {
            "username": "test_updated",
            "email": "test@user.com",
            "bio": "testing bio",
        }
        response = self.client.post(self.url, updated_user_data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, updated_user_data["username"])
        self.assertEqual(self.user.bio, updated_user_data["bio"])

    def test_staff_update_user(self):
        self.client.login(email=self.moderator.email, password="Test-123")
        updated_user_data = {
            "username": "test_moderation",
            "email": "test@user.com",
            "bio": "created by moderator",
        }
        response = self.client.post(self.url, updated_user_data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, updated_user_data["username"])
        self.assertEqual(self.user.bio, updated_user_data["bio"])
