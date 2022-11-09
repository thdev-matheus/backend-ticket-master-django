from comments.models import Comment
from rest_framework import serializers
from tickets.serializers import TicketSerializer
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "created_at",
            "ticket",
            "user",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]
