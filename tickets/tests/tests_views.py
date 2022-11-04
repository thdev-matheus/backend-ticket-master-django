from rest_framework.test import APITestCase
from users.models import User
from model_bakery import baker
from departments.models import Department


class TicketViewTest(APITestCase):
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
        
        cls.department = Department.objects.create(name="departamento")        
        cls.ticket = baker.make('tickets.Ticket', support_department=cls.department)

    def setUp(self) -> None:
        login_admin = self.client.post("/api/login/", self.user_admin_data_login)
        login_non_admin = self.client.post(
            "/api/login/", self.user_non_admin_data_login
        )

        self.token_admin = f"Token {login_admin.data['token']}"
        self.token_non_admin = f"Token {login_non_admin.data['token']}"

    def test_create_ticket_correct_data(self):
        """
        Criar ticket com os dados corretos.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.post("/api/tickets/", {"description":"descrição"})
        expected_keys = {"id","description","is_solved","created_at","urgency","status","support_department","support","user"}
        received_keys = set(response.data.keys())

        self.assertEqual(201, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_creation_a_ticket_without_data(self):
        """
        Criar ticket com os dados incorretos.
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.post("/api/tickets/", {})
        self.assertEqual(400, response.status_code)
        self.assertIn("description", response.data)
        self.assertEqual("required", response.data["description"][0].code)

    def test_creation_ticket_without_token(self):
        """
        Criar ticket sem token.
        """
        response = self.client.post("/api/tickets/", {})
        self.assertEqual(401, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_authenticated", response.data["detail"].code)

    def test_list_all_tickets_with_admin_token(self):
        """
        Listar todos os tickets como adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get("/api/tickets/")

        self.assertEqual(200, response.status_code)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_list_all_tickets_with_a_non_admin_token(self):
        """
        Listar todos os tickets sem ser adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get("/api/tickets/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)


    def test_retrieve_ticket_by_id_with_admin_token(self):
        """
        Listar um tickets sendo adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/tickets/{self.ticket.id}/")
        expected_keys = {"id","description","is_solved","created_at","urgency","status","support_department","support","user"}
        received_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_retrieve_ticket_by_id_with_non_admin_token(self):
        """
        Listar um tickets sem ser adm, e sem ser do mesmo departamento
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/tickets/{self.ticket.id}/")
        
        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_retrieve_ticket_that_not_exist(self):
        """
        Listar um tickets que não existe
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/tickets/1111111-111-1111111-1111/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)


    def test_soft_delete_user_with_non_admin_token(self):
        """
        Soft delete com usuário sem permissão
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_soft_delete_ticket_with_admin_token(self):
        """
        Soft delete com usuário sendo adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.delete(f"/api/tickets/{self.ticket.id}/")
        expected_keys = {"description","is_solved","urgency","support_department","support","user"}
        received_keys = set(response.data.keys())

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.data["is_solved"])
        self.assertSetEqual(expected_keys, received_keys)

    def test_soft_delete_ticket_that_not_exist(self):
        """
        Soft delete em um ticket que não existe
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.delete(f"/api/tickets/1111111-111-1111111-1111/")

        self.assertEqual(404, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("not_found", response.data["detail"].code)
        
    def test_list_summary_tickets_with_admin_token(self):
        """
        Listar os totais de tickets abertos de cada departamento sendo adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get("/api/summary/tickets/")

        self.assertEqual(200, response.status_code)
        
    def test_list_summary_tickets_non_admin_token(self):
        """
        Listar os totais de tickets abertos de cada departamento sem permissão
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get("/api/summary/tickets/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)
        
    def test_retrieve_tickets_from_apartments_admin(self):
        """
        Listar todos os tickets de um departmento sendo adm
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/tickets/department/{self.department.id}/")

        self.assertEqual(200, response.status_code)

    def test_retrieve_tickets_from_apartments_not_admin(self):
        """
        Listar todos os tickets de um departmento sem permissão
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/tickets/department/{self.department.id}/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)

    def test_retrieve_open_tickets_with_urgency_admin(self):
        """
        Lista o ticket aberto, de maior urgencia, mais antigo, sendo admin
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.get(f"/api/tickets/department/{self.department.id}/newest/")

        self.assertEqual(200, response.status_code)
        
    def test_retrieve_open_tickets_with_urgency_non_admin(self):
        """
        Lista o ticket aberto, de maior urgencia, mais antigo, sem permissão
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.get(f"/api/tickets/department/{self.department.id}/newest/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)
        
    def test_retrieve_ticket_and_add_support(self):
        """
        Lista o ticket mais urgente e associa o owner do Token ao campo "support_user"
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_admin)
        response = self.client.patch(f"/api/tickets/{self.ticket.id}/")

        expected_keys = {"description","is_solved","urgency","support"}
        received_keys = set(response.data.keys())
        self.assertEqual(200, response.status_code)
        self.assertSetEqual(expected_keys, received_keys)
    
    def test_retrieve_ticket_and_add_support_without_permission(self):
        """
        Lista o ticket mais urgente e associa o owner do Token ao campo "support_user" sem permissão
        """
        self.client.credentials(HTTP_AUTHORIZATION=self.token_non_admin)
        response = self.client.patch(f"/api/tickets/{self.ticket.id}/")

        self.assertEqual(403, response.status_code)
        self.assertIn("detail", response.data)
        self.assertEqual("permission_denied", response.data["detail"].code)