import ipdb
from comments.models import Comment
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker
from tickets.models import Ticket


class CommentModelTest(TestCase):
    def test_comment_fields(self):
        comment = baker.make("comments.Comment")
        expected_fields = {
            "_state",
            "id",
            "content",
            "created_at",
            "ticket_id",
            "user_id",
        }
        received_fields = set(vars(comment).keys())

        self.assertSetEqual(expected_fields, received_fields)

    def test_create_comment_whithout_user_or_ticket_relation(self):

        with self.assertRaises(ValidationError):
            comment = Comment(content="teste")
            comment.full_clean()
