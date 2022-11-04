import ipdb
from model_bakery import baker
from rest_framework.test import APITestCase

from tickets.models import Ticket, UrgencyCategories
from users.models import User


class SolutionsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_admin = User.objects.create_superuser(
            username="AdminUser", password="1234"
        )
        cls.user_non_admin1 = User.objects.create_user(
            username="NonAdminUser1", password="1234"
        )
        cls.user_non_admin2 = User.objects.create_user(
            username="NonAdminUser2", password="1234"
        )
        cls.user_non_admin3 = User.objects.create_user(
            username="NonAdminUser3", password="1234"
        )

        cls.user_admin_data_login = {
            "username": cls.user_admin.username,
            "password": "1234",
        }

        cls.user_non_admin1_data_login = {
            "username": cls.user_non_admin1.username,
            "password": "1234",
        }
        cls.user_non_admin2_data_login = {
            "username": cls.user_non_admin2.username,
            "password": "1234",
        }
        cls.user_non_admin3_data_login = {
            "username": cls.user_non_admin3.username,
            "password": "1234",
        }

        cls.ticket_1 = baker.make(
            "tickets.Ticket",
            urgency=UrgencyCategories.DEFAULT,
            user=cls.user_non_admin1,
        )
        cls.ticket_2 = baker.make(
            "tickets.Ticket",
            urgency=UrgencyCategories.AVERAGE,
            user=cls.user_non_admin2,
        )
        cls.ticket_3 = baker.make(
            "tickets.Ticket", urgency=UrgencyCategories.HIGH, user=cls.user_non_admin3
        )

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        self.token_admin = f"Token {login_admin.data['token']}"

        login_non_admin1 = self.client.post(
            "/api/login/", self.user_non_admin1_data_login
        )
        self.token_non_admin1 = f"Token {login_non_admin1.data['token']}"

        login_non_admin2 = self.client.post(
            "/api/login/", self.user_non_admin2_data_login
        )
        self.token_non_admin2 = f"Token {login_non_admin2.data['token']}"

        login_non_admin3 = self.client.post(
            "/api/login/", self.user_non_admin3_data_login
        )
        self.token_non_admin3 = f"Token {login_non_admin3.data['token']}"

    def test_():
        ...
