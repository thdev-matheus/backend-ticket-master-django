from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "support_department",
            "is_superuser",
            "password",
        ]
        read_only_fields = [
            "id",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        model = self.Meta.model
        instance = model.objects.create_user(**validated_data)
        return instance


class UserPatchActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_active",
            "date_joined",
            "support_department",
        ]


class UserSerializerSupport(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
        read_only_fields = [
            "id",
            "username",
        ]
