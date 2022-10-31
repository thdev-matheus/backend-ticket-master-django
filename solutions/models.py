from django.db import models
import uuid

class Solution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    solved_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.CharField(max_length=30)
    ticket_id = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="solution"
    )
    user_id = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="solved_by"
    )

