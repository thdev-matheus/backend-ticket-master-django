import uuid

from django.db import models


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_id = models.ForeignKey(
        "tickets.Ticket", on_delete=models.CASCADE, related_name="comments"
    )
