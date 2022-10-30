from django.db import models
import uuid

class UrgencyCategories(models.TextChoices):
    HIGH = "High"
    AVERAGE = "Average"
    DEFAULT = "Low"

class Ticket(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    is_solved = models.BooleanField(default=False)
    solution = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    urgency = models.CharField(max_length=20,choices=UrgencyCategories.choices, default=UrgencyCategories.DEFAULT)
    department_id = models.ForeignKey("departments.department", on_delete=models.CASCADE,blank=True, null=True, related_name="departments")