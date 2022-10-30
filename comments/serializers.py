from rest_framework import serializers

from comments.models import Comment
from tickets.serializers import TicketSerializer

class CommentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    ticket = TicketSerializer(source="user", read_only=True)

    class Meta:
            model = Comment
            fields = ["id","content", "created_at", "ticket_id"]
            read_only_fields = ["id", "created_at"]