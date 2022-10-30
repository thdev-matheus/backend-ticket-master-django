from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=20, unique=True)
    is_adm = models.BooleanField(default=False)
    department_id = models.ForeignKey("departments.department", on_delete=models.CASCADE,blank=True, null=True, related_name="departments")

    REQUIRED_FIELDS = ["username"]