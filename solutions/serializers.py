import datetime
import math

import ipdb
from rest_framework import serializers

from solutions.models import Solution
from tickets.models import Ticket
from tickets.serializers import TicketSerializerDetailed, TicketSerializerNoSupport
from users.serializers import UserSerializer


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ["id", "description", "solved_at", "time_taken", "ticket", "user"]
        read_only_fields = ["id", "solved_at"]

    time_taken = serializers.SerializerMethodField()

    def get_time_taken(self, obj):
        ticket = Ticket.objects.get(id=obj.ticket.id)
        time_to_solve = obj.solved_at - ticket.created_at
        days = math.floor(time_to_solve.seconds / 86400)
        hours = math.floor(time_to_solve.seconds % 86400 / 3600)
        minutes = math.floor(time_to_solve.seconds % 3600 / 60)
        seconds = math.floor(time_to_solve.seconds % 60)
        return f"{days} days and {hours}:{minutes}:{seconds}"


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
        ticket = Ticket.objects.get(id=obj.ticket.id)
        time_to_solve = obj.solved_at - ticket.created_at
        days = math.floor(time_to_solve.seconds / 86400)
        hours = math.floor(time_to_solve.seconds % 86400 / 3600)
        minutes = math.floor(time_to_solve.seconds % 3600 / 60)
        seconds = math.floor(time_to_solve.seconds % 60)
        return f"{days} days and {hours}:{minutes}:{seconds}"


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
        ticket = Ticket.objects.get(id=obj.ticket.id)
        time_to_solve = obj.solved_at - ticket.created_at
        days = math.floor(time_to_solve.seconds / 86400)
        hours = math.floor(time_to_solve.seconds % 86400 / 3600)
        minutes = math.floor(time_to_solve.seconds % 3600 / 60)
        seconds = math.floor(time_to_solve.seconds % 60)
        return f"{days} days and {hours}:{minutes}:{seconds}"
