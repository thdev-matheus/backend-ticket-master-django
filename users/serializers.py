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
            "is_active",
        ]
        read_only_fields = [
            "id",
            "is_superuser",
            "is_active",
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
            "is_active",
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
