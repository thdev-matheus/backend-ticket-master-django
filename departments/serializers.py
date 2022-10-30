from rest_framework import serializers
from departments.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
            model = Department
            fields = ["id","name", "is_active"]
            read_only_fields = ["id"]