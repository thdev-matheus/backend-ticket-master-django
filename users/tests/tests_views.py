import ipdb
from model_bakery import baker
from rest_framework.test import APITestCase
from users.models import User


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_admin = User.objects.create_superuser(
            username="AdminUser", password="1234"
        )

        cls.user_admin_data_login = {
            "username": cls.user_admin.username,
            "password": "1234",
        }

    def test_login_with_correct_data(self):
        response = self.client.post("/api/login/", self.user_admin_data_login)

        self.assertEqual(200, response.status_code)
        self.assertIn("token", response.data)

    def test_login_with_incorrect_credentials(self):
        response = self.client.post(
            "/api/login/",
            {"username": self.user_admin.username, "password": "123456789"},
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual("authorization", response.data["non_field_errors"][0].code)

    def test_login_without_fields(self):
        response = self.client.post("/api/login/", {})

        self.assertEqual(400, response.status_code)
        self.assertIn("username", response.data)
        self.assertEqual("required", response.data["username"][0].code)
        self.assertIn("password", response.data)
        self.assertEqual("required", response.data["password"][0].code)
