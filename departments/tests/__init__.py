import ipdb
from departments.models import Department
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker


class DepartmentModelTest(TestCase):
    def test_creation_of_a_department(self):
        dep = baker.make("departments.Department")
        expected_keys = {
            "_state",
            "id",
            "name",
            "is_active",
        }
        received_keys = set(vars(dep).keys())

        self.assertSetEqual(expected_keys, received_keys)
        self.assertTrue(dep.is_active)

    def test_max_length_name(self):
        with self.assertRaises(ValidationError):
            dep = Department(name="string_de_teste_com_mais_de_20_caracteres")
            dep.full_clean()
