from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class TestRegisterUser(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.url = reverse("register")

    def test_register_user(self):
        user_data = {
            "username": "kamil",
            "email": "kamil@user.com",
            "password1": "Test-123",
            "password2": "Test-123",
        }
        response = self.client.post(self.url, user_data)
        created_user = User.objects.get(id=1)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(created_user)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_register_with_invalid_data(self):
        user_data = {
            "username": "kamil",
            "email": "kamiluser.com",
            "password1": "test-123",
            "password2": "test-123",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("_auth_user_id" not in self.client.session)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=1)
