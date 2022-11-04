from rest_framework import serializers

<<<<<<< HEAD
=======
from departments.models import Department
from tickets.models import Ticket
>>>>>>> 985e39a4d2a9fb9dd9edb6b6d9bd4221e8c73163
from users.serializers import UserSerializer, UserSerializerSupport


from utils.mixins import get_ticket_status

class TicketSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
	class Meta:
		model = Ticket
		fields = ["id","description", "is_solved","created_at","urgency", "status", "support_department", "user", "support"]
		read_only_fields = ["id", "created_at"]

	status = serializers.SerializerMethodField()

	def get_status(self, obj):
		return get_ticket_status(self, obj)

class TicketSerializerDetailed(serializers.ModelSerializer):
	class Meta:
		model = Ticket
		fields = ["id","description", "is_solved","created_at","urgency", "status", "support_department", "user", "support"]
		read_only_fields = ["id", "is_solved", "created_at"]
		depth = 1
        
	user = UserSerializer(read_only=True)
	support = UserSerializer(read_only=True)
	status = serializers.SerializerMethodField()

	def get_status(self, obj):
		return get_ticket_status(self, obj)
=======
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "support_department",
            "user",
            "support",
        ]
        read_only_fields = ["id", "created_at"]


class TicketSerializerDetailed(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "support_department",
            "user",
            "support",
        ]
        read_only_fields = ["id", "is_solved", "created_at"]
        depth = 1

    user = UserSerializer(read_only=True)
    support = UserSerializer(read_only=True)
>>>>>>> 985e39a4d2a9fb9dd9edb6b6d9bd4221e8c73163


class TicketSerializerNoDepartment(serializers.ModelSerializer):
<<<<<<< HEAD
	class Meta:
		model = Ticket
		fields = ["id","description", "is_solved","created_at","urgency", "status", "user", "support"]
		read_only_fields = ["id", "created_at"]
		depth = 1
        
	user = UserSerializer(read_only=True)
	support = UserSerializerSupport(read_only=True)
	status = serializers.SerializerMethodField()
	
	def get_status(self, obj):
		return get_ticket_status(self, obj)
=======
    class Meta:
        model = Ticket
        fields = [
            "id",
            "description",
            "is_solved",
            "created_at",
            "urgency",
            "user",
            "support",
        ]
        read_only_fields = ["id", "created_at"]
        depth = 1

    user = UserSerializer(read_only=True)
    support = UserSerializerSupport(read_only=True)
>>>>>>> 985e39a4d2a9fb9dd9edb6b6d9bd4221e8c73163


class TicketSerializerNoSupport(serializers.ModelSerializer):
<<<<<<< HEAD
	class Meta:
		model = Ticket
		fields = ["id","description", "is_solved","created_at","urgency", "status", "user"]
		read_only_fields = ["id", "created_at"]
		depth = 1
        
	user = UserSerializer(read_only=True)
	status = serializers.SerializerMethodField()
	
	def get_status(self, obj):
		return get_ticket_status(self, obj)
=======
    class Meta:
        model = Ticket
        fields = ["id", "description", "is_solved", "created_at", "urgency", "user"]
        read_only_fields = ["id", "created_at"]
        depth = 1
>>>>>>> 985e39a4d2a9fb9dd9edb6b6d9bd4221e8c73163

    user = UserSerializer(read_only=True)
