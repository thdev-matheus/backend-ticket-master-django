from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
            model = User
            fields = ["id","username", "is_adm", "department_id", "is_superuser", "password"]
            read_only_fields = ["id", "is_superuser"]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user