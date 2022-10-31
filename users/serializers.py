from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
            model = User
            fields = ["id","username", "department_id", "is_superuser", "password"]
            read_only_fields = ["id", "is_superuser"]


    def create(self, validated_data:dict):
        return User.objects.create_user(**validated_data)
