import uuid

from django.db import models


class Solution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    solved_at = models.DateTimeField(auto_now_add=True)
    ticket = models.OneToOneField(
        "tickets.Ticket",
        on_delete=models.CASCADE,
    )
    solver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="solved_by",
    )

    class Meta:
        ordering = ["id"]
