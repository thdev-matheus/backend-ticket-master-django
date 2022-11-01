from rest_framework import serializers

from tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields = ["id","description", "is_solved","created_at","urgency", "department"]
            read_only_fields = ["id", "created_at"]