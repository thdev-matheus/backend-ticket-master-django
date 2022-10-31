import ipdb
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker
from tickets.models import Ticket, UrgencyCategories


class TicketModelTest(TestCase):
    def test_creation_of_a_ticket(self):
        ticket = baker.make("tickets.Ticket")
        expected_keys = {
            "_state",
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "department_id",
            "user_id",
        }
        received_keys = set(vars(ticket).keys())

        self.assertSetEqual(expected_keys, received_keys)
        self.assertFalse(ticket.is_solved)
