from rest_framework import serializers

from tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields = ["id","description", "is_solved", "solution","created_at","urgency", "department_id"]
            read_only_fields = ["id", "created_at"]