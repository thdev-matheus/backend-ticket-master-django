from rest_framework import serializers

from solutions.models import Solution

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "description", "solved_at", "time_taken", "ticket_id", "user_id"]
        read_only_fields = ["id", "solved_at"]