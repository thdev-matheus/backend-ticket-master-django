from rest_framework import serializers

from users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "department", "is_superuser", "password"]
        read_only_fields = ["id", "is_superuser"]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        model = self.Meta.model
        instance = model.create_user(**validated_data)
        return instance


class UserPatchActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_active", "date_joined", "department"]
