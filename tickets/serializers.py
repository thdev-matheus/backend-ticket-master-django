from rest_framework import serializers
from departments.models import Department
from users.serializers import UserSerializer, UserSerializerSupport

from tickets.models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields = ["id","description", "is_solved","created_at","urgency", "support_department", "user", "support"]
            read_only_fields = ["id", "created_at"]
        

class TicketSerializerDetailed(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields = ["id","description", "is_solved","created_at","urgency", "support_department", "user", "support"]
            read_only_fields = ["id", "is_solved", "created_at"]
            depth = 1
        
    user = UserSerializer(read_only=True)
    support = UserSerializer(read_only=True)

class TicketSerializerNoDepartment(serializers.ModelSerializer):
    class Meta:
            model = Ticket
            fields = ["id","description", "is_solved","created_at","urgency", "user", "support"]
            read_only_fields = ["id", "created_at"]
            depth = 1
        
    user = UserSerializer(read_only=True)
    support = UserSerializerSupport(read_only=True)

            
        
