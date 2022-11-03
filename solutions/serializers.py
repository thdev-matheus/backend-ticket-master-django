from rest_framework import serializers

from solutions.models import Solution

from tickets.serializers import TicketSerializerDetailed, TicketSerializerNoSupport

from users.serializers import UserSerializer

class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "description", "solved_at", "time_taken", "ticket", "user"]
        read_only_fields = ["id", "solved_at"]

    time_taken = serializers.SerializerMethodField()

    def get_time_taken(self, obj):
        return 1

class SolutionSerializerDetailedNoSupport(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "description", "solved_at", "time_taken", "user", "ticket"]
        read_only_fields = ["id", "solved_at"]
        depth = 1

    user = UserSerializer(read_only=True)
    ticket = TicketSerializerNoSupport(read_only=True)

    time_taken = serializers.SerializerMethodField()

    def get_time_taken(self, obj):
        return 1

class SolutionSerializerDetailed(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "description", "solved_at", "time_taken", "user", "ticket"]
        read_only_fields = ["id", "solved_at"]
        depth = 1

    user = UserSerializer(read_only=True)
    ticket = TicketSerializerDetailed(read_only=True)

    time_taken = serializers.SerializerMethodField()

    def get_time_taken(self, obj):
        return 1