import uuid

from django.db import models


class Department(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
