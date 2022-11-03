from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from tickets.models import Ticket
from departments.models import Department
import ipdb
from django.forms import model_to_dict


class CommentsCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.department = Department.objects.create(name="IT")

        cls.user = User.objects.create_user(username="noAdminUser", password="1234")
        cls.user2 = User.objects.create_user(username="bruno", password="1234")

        cls.ticket = Ticket.objects.create(
            description="Ticket test description",
            urgency="High",
            support_department=cls.department,
            user=cls.user,
        )

        cls.register_url = f"/api/comment/register/{cls.ticket.id}/"

        cls.user_data_login = {
            "username": cls.user.username,
            "password": "1234",
        }

        cls.user_data_login2 = {
            "username": cls.user2.username,
            "password": "1234",
        }

        cls.comment_data = {
            "content": "User do not respond",
            "ticket": cls.ticket,
            "user": cls.user,
        }

        cls.comment_data2 = {
            "content": "User is out of office",
            "ticket": cls.ticket,
            "user": cls.user,
        }

        cls.new_comment_data = {
            "content": "User is out - Comment edit"
        }

    def test_create_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_create_comment_with_correct_data(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)

        expected_keys = {"id", "user", "created_at", "content", "ticket"}

        received_keys = set(response.data.keys())

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_create_a_comment_without_data(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)
        response = self.client.post(self.register_url, {})

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_create_a_comment_without_token(self):
        self.client.post("/api/login/", self.user_data_login)

        response = self.client.post(self.register_url, self.comment_data)

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_list_a_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)

        comment_id = response.data["id"]
        comment_data = self.client.get(f"/api/comment/{comment_id}/")

        expected_status_code = status.HTTP_200_OK
        result_status_code = comment_data.status_code

        expected_keys = {"id", "user", "created_at", "content", "ticket"}

        received_keys = set(comment_data.data.keys())

        self.assertEqual(expected_status_code, result_status_code)
        self.assertSetEqual(expected_keys, received_keys)

    def test_list_a_non_exist_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        self.client.post(self.register_url, self.comment_data)

        comment_data = self.client.get(f"/api/comment/123456/")

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = comment_data.status_code

        self.assertEqual(expected_status_code, result_status_code)
    
    def test_list_a_exist_comment_with_a_owner_token(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)
        comment_id = response.data["id"]
        comment_data = self.client.get(f"/api/comment/{comment_id}/")

        expected_status_code = status.HTTP_200_OK
        result_status_code = comment_data.status_code

        self.assertEqual(expected_status_code, result_status_code)
    
    def test_list_a_exist_comment_without_owner_token(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login2)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)
        comment_id = response.data["id"]

        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        comment_data = self.client.get(f"/api/comment/{comment_id}/")

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = comment_data.status_code

        self.assertEqual(expected_status_code, result_status_code)


    def test_edit_a_exist_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login2)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)

        comment_id = response.data["id"]
        comment_response = self.client.patch(f"/api/comment/{comment_id}/", self.new_comment_data)

        expected_status_code = status.HTTP_200_OK
        result_status_code = comment_response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_edit_a_non_exist_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login2)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        self.client.post(self.register_url, self.comment_data)

        comment_response = self.client.patch(f"/api/comment/123456/", self.new_comment_data)

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = comment_response.status_code

        self.assertEqual(expected_status_code, result_status_code)
    

    def test_delete_a_exist_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login2)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        response = self.client.post(self.register_url, self.comment_data)

        comment_id = response.data["id"]
        comment_response = self.client.delete(f"/api/comment/{comment_id}/")

        expected_status_code = status.HTTP_204_NO_CONTENT
        result_status_code = comment_response.status_code

        self.assertEqual(expected_status_code, result_status_code)

    def test_delete_a_non_exist_comment(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login2)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        self.client.post(self.register_url, self.comment_data)

        comment_response = self.client.delete(f"/api/comment/123456/")

        expected_status_code = status.HTTP_404_NOT_FOUND
        result_status_code = comment_response.status_code

        self.assertEqual(expected_status_code, result_status_code)


    def test_get_all_user_comments(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        self.client.post(self.register_url, self.comment_data)
        self.client.post(self.register_url, self.comment_data2)

        user_comments = self.client.get(f"/api/comment/user/{self.user.id}/")

        expected_status_code = status.HTTP_200_OK
        result_status_code = user_comments.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(2, user_comments.data["count"])
        
    def test_get_all_ticket_comments(self):
        response_user_login = self.client.post("/api/login/", self.user_data_login)
        user_token = f"Token {response_user_login.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=user_token)

        self.client.post(self.register_url, self.comment_data)
        self.client.post(self.register_url, self.comment_data2)

        ticket_comments = self.client.get(f"/api/comment/ticket/{self.ticket.id}/")

        expected_status_code = status.HTTP_200_OK
        result_status_code = ticket_comments.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(2, ticket_comments.data["count"])
        

        

        
