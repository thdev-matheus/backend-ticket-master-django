from rest_framework import serializers

from comments.models import Comment
from tickets.serializers import TicketSerializer
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    ticket = TicketSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
            model = Comment
            fields = ["id","content", "created_at", "ticket", "user"]
            read_only_fields = ["id", "created_at"]