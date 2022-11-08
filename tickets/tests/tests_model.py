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
            "support_department_id",
            "support_user_id",
            "owner_id",
        }
        received_keys = set(vars(ticket).keys())

        self.assertSetEqual(expected_keys, received_keys)
        self.assertFalse(ticket.is_solved)

    def test_create_ticket_with_wrong_urgency(self):
        with self.assertRaises(ValidationError):
            ticket = Ticket(description="descrição", urgency="chave_errada")
            ticket.full_clean()

    def test_create_ticket_without_description(self):
        with self.assertRaises(ValidationError):
            ticket = Ticket(urgency=UrgencyCategories.DEFAULT)
            ticket.full_clean()
