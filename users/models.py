import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    department_id = models.ForeignKey(
        "departments.Department",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="users",
    )
