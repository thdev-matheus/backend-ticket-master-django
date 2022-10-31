import ipdb
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker
from users.models import User


class UserModelTest(TestCase):
    def test_keys_of_abstract_user(self):
        user = baker.make("users.User")
        expected_keys = {
            "is_superuser",
            "is_staff",
            "is_active",
            "first_name",
            "email",
            "last_name",
            "id",
            "date_joined",
            "username",
            "_state",
            "department_id",
            "last_login",
            "password",
        }
        received_keys = set(vars(user).keys())

        self.assertSetEqual(expected_keys, received_keys)
