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

        cls.department_data = {
            "name": "TI",
        }

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )

        self.token_admin = f"Token {login_admin.data['token']}"
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

    def test_creation_department_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.post("/api/department/", self.department_data)
        expected_keys = {
            "id",
            "name",
            "is_active",
        }
        received_keys = set(response.data.keys())

        self.assertSetEqual(expected_keys, received_keys)
        self.assertTrue(response.data["is_active"])

    def test_creation_department_with_non_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.post("/api/department/", self.department_data)

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_creation_department_without_token(self):
        response = self.client.post("/api/department/", self.department_data)

        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_creation_department_without_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.post("/api/department/", {})

        self.assertEqual(400, response.status_code)
        self.assertIn("name", response.data)
        self.assertEqual("required", response.data["name"][0].code)


class PatchDeleteDepartmentViewTest(APITestCase):
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

        cls.department_patch_data = {
            "name": "Nome Atualizado",
        }

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        self.token_admin = f"Token {login_admin.data['token']}"

        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        department_response = self.client.post("/api/department/", {"name": "TI"})
        self.department = department_response.data

        self.client.credentials(HTTP_AUTHORIZATION=None)

    def test_retrieve_department_with_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/department/{self.department['id']}/")
        expected_keys = {
            "id",
            "name",
            "is_active",
        }
        received_keys = set(response.data.keys())

        self.assertSetEqual(expected_keys, received_keys)
        self.assertTrue(response.data["is_active"])

    def test_retrieve_department_with_non_admin_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/department/{self.department['id']}/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_retrieve_department_that_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/department/id_que_não_existe/")
        ipdb.set_trace()
        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)

    def test_retrieve_department_whitout_token(self):
        ...

    def test_update_department_with_admin_token(self):
        ...

    def test_update_department_with_non_admin_token(self):
        ...

    def test_update_department_that_not_exist(self):
        ...

    def test_update_department_whitout_token(self):
        ...

    def test_soft_delete_department_with_admin_token(self):
        ...

    def test_soft_delete_department_with_non_admin_token(self):
        ...

    def test_soft_delete_department_that_not_exist(self):
        ...

    def test_soft_delete_department_whitout_token(self):
        ...
