from rest_framework import serializers
from tickets.models import Ticket
from users.serializers import UserSerializer, UserSerializerSupport
from utils.mixins import get_ticket_status


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "status",
            "support_department",
            "user",
            "support",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]

    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_ticket_status(self, obj)


class TicketSerializerDetailed(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "status",
            "support_department",
            "user",
            "support",
        ]
        read_only_fields = [
            "id",
            "is_solved",
            "created_at",
        ]
        depth = 1

    user = UserSerializer(read_only=True)
    support = UserSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_ticket_status(self, obj)


class TicketSerializerNoDepartment(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "status",
            "user",
            "support",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
        depth = 1

    user = UserSerializer(read_only=True)
    support = UserSerializerSupport(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_ticket_status(self, obj)


class TicketSerializerNoSupport(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "status",
            "user",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
        depth = 1

    user = UserSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return get_ticket_status(self, obj)
