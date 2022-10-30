from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Comment(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_id = models.ForeignKey("tickets.ticket", on_delete=models.CASCADE, related_name="tickets")
