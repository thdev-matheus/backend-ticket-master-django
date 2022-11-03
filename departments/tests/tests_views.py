import ipdb
from rest_framework.test import APITestCase

from users.models import User


class CreateDepartmentViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_admin = User.objects.create_superuser(
            username="AdminUser", password="1234"
        )
        cls.user_non_admin = User.objects.create_user(
            username="NonAdminUser", password="1234"
        )

        cls.user_admin_data_login = {
            "username": cls.user_admin.username,
            "password": "1234",
        }

        cls.user_non_admin_data_login = {
            "username": cls.user_non_admin.username,
            "password": "1234",
        }

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )

        self.token_admin = f"Token {login_admin.data['token']}"
        self.token_non_admin = f"Token {login_non_admin.data['token']}"
