import uuid

from django.db import models

class UrgencyCategories(models.TextChoices):
    HIGH = "High"
    AVERAGE = "Average"
    DEFAULT = "Low"

class Ticket(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    urgency = models.CharField(
        max_length=20,
        choices=UrgencyCategories.choices,
        default=UrgencyCategories.DEFAULT,
    )
    support_department = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="tickets",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="tickets",
    )
    support = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="supported_by",
    )
