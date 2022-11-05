from departments.models import Department
from model_bakery import baker
from rest_framework.test import APITestCase
from tickets.models import UrgencyCategories
from users.models import User


class SolutionsViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.department = Department.objects.create(name="departamento")

        cls.user_admin = User.objects.create_superuser(
            username="AdminUser", password="1234", department=cls.department
        )
        cls.user_non_admin = User.objects.create_user(
            username="NonAdminUser", password="1234"
        )
        cls.user_non_admin2 = User.objects.create_user(
            username="NonAdminUser2", password="1234"
        )

        cls.user_admin_data_login = {
            "username": cls.user_admin.username,
            "password": "1234",
        }

        cls.user_non_admin_data_login = {
            "username": cls.user_non_admin.username,
            "password": "1234",
        }

        cls.ticket = baker.make(
            "tickets.Ticket",
            urgency=UrgencyCategories.DEFAULT,
            user=cls.user_non_admin,
            support_department=cls.department,
        )
        cls.ticket2 = baker.make(
            "tickets.Ticket",
            urgency=UrgencyCategories.AVERAGE,
            user=cls.user_non_admin2,
            support_department=cls.department,
            is_solved=True,
        )
        cls.solution = baker.make(
            "solutions.Solution",
            ticket=cls.ticket2,
            user=cls.user_non_admin2,
        )

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        self.token_admin = f"Token {login_admin.data['token']}"

        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

    def test_create_solution_without_data(self):
        """
        Criar solution sem data
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        data = {}
        response = self.client.post("/api/solutions/", data)

        self.assertEqual(400, response.status_code)
        self.assertIn("description", response.data)
        self.assertEqual("required", response.data["description"][0].code)

    def test_create_solution(self):
        """
        Criar solution dados corretos
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        data = {"description": "just switch it on/off", "ticket": self.ticket.id}
        response = self.client.post("/api/solutions/", data)
        expected_keys = {
            "id",
            "description",
            "solved_at",
            "time_taken",
            "ticket",
            "user",
        }
        received_keys = set(response.data.keys())

        self.assertEqual(201, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_list_all_solution_with_admin_token(self):
        """
        Listar todos os solutions como adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get("/api/solutions/")

        self.assertEqual(200, response.status_code)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_list_all_solution_with_a_non_admin_token(self):
        """
        Listar todos os solutions sem ser adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get("/api/solutions/")

        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("error", response.data["detail"].code)

    def test_list_a_solution_with_admin_token(self):
        """
        Listar uma solution como adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solutions/{self.solution.id}/")
        expected_keys = {
            "id",
            "description",
            "solved_at",
            "time_taken",
            "ticket",
            "user",
        }
        received_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_list_a_solution_with_a_non_admin_token(self):
        """
        Listar um solution sem ser adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/solutions/{self.solution.id}/")

        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("error", response.data["detail"].code)

    def test_list_a_solution_that_not_exist(self):
        """
        Listar uma solution que não existe
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solutions/00000/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)

    def test_list_a_solution_by_ticket_with_admin_token(self):
        """
        Listar uma solution pelo ticket como adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solution/ticket/{self.ticket2.id}/")
        expected_keys = {
            "id",
            "description",
            "solved_at",
            "time_taken",
            "ticket",
            "user",
        }
        received_keys = set(response.data.keys())
        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_list_a_solution_by_ticket_with_a_non_admin_token(self):
        """
        Listar um solution sem ser adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/solution/ticket/{self.ticket2.id}/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_list_a_solution_by_ticket_that_not_exist(self):
        """
        Listar uma solution em que o ticket que não existe
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solution/ticket/00000/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)

    def test_list_a_solution_by_department_with_admin_token(self):
        """
        Listar uma solution pelo departamento como adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solutions/department/{self.department.id}/")
        self.assertEqual(200, response.status_code)

    def test_list_a_solution_by_department_with_a_non_admin_token(self):
        """
        Listar um solution sem ser adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/solutions/department/{self.department.id}/")
        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("error", response.data["detail"].code)

    def test_list_a_solution_by_department_that_not_exist(self):
        """
        Listar uma solution pelo departamento que não existe
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/solutions/department/00000/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)
