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


class UserViewTest(APITestCase):
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

        cls.test_data = {
            "username": "teste",
            "password": "teste",
        }

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )

        self.token_admin = f"Token {login_admin.data['token']}"
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

    def test_creation_a_user_with_correct_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.post("/api/users/", self.test_data)
        expected_keys = {
            "id",
            "username",
            "department",
            "is_superuser",
        }
        received_keys = set(response.data.keys())

        self.assertEqual(201, response.status_code)
        self.assertNotIn("password", response.data)
        self.assertSetEqual(expected_keys, received_keys)

    def test_creation_a_user_without_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.post("/api/users/", {})
        self.assertEqual(400, response.status_code)
        self.assertIn("username", response.data)
        self.assertEqual("required", response.data["username"][0].code)
        self.assertIn("password", response.data)
        self.assertEqual("required", response.data["password"][0].code)

    def test_creation_a_user_without_token(self):
        response = self.client.post("/api/users/", {})
        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_creation_a_user_with_a_non_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.post("/api/users/", self.test_data)

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_list_all_users_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get("/api/users/")

        self.assertEqual(200, response.status_code)
        self.assertIn("count", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("next", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(2, response.data["count"])

    def test_list_all_users_with_a_non_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get("/api/users/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)


class UserDeleteViewTest(APITestCase):
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

        cls.test_update_data = {
            "username": "user atualizado",
        }

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )

        self.token_admin = f"Token {login_admin.data['token']}"
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

    def test_retrieve_user_by_id_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/users/{self.user_non_admin.id}/")
        expected_keys = {
            "id",
            "username",
            "department",
            "is_superuser",
        }
        received_keys = set(response.data.keys())
        # ipdb.set_trace()
        self.assertEqual(200, response.status_code)
        self.assertNotIn("password", response.data)
        self.assertSetEqual(expected_keys, received_keys)

    def test_retrieve_user_by_id_with_non_admin_token(self):
        ...

    def test_retrieve_user_that_not_exist(self):
        ...

    def test_update_user_with_non_admin_token(self):
        ...

    def test_update_user_with_admin_token(self):
        ...

    def test_update_user_that_not_exist(self):
        ...

    def test_soft_delete_user_with_non_admin_token(self):
        ...

    def test_soft_delete_user_with_admin_token(self):
        ...

    def test_soft_delete_user_that_not_exist(self):
        ...


class UserReactivateViewTest(APITestCase):
    ...
