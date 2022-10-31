import uuid

from django.db import models


class Solution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    solved_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.CharField(max_length=30)
    ticket = models.OneToOneField(
        "tickets.Ticket",
        on_delete=models.CASCADE,
    )
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
    )
