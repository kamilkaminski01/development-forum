from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class TestLoginUser(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("login")
        self.user = User.objects.create(  # type: ignore
            email="test@user.com",
            username="test",
        )
        self.user.set_password("Test-123")
        self.user.save()

    def test_login_user(self):
        user_data = {
            "email": "test@user.com",
            "password": "Test-123",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_with_invalid_data(self):
        user_data = {
            "email": "testuser.com",
            "password": "test-123",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("_auth_user_id" not in self.client.session)
