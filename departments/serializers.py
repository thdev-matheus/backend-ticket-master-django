from departments.models import Department
from rest_framework import serializers


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "is_active",
        ]
