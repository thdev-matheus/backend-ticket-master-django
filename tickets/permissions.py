from rest_framework import permissions
from rest_framework.views import Request, View

from tickets.models import Ticket
from users.models import User

class IsOwnerOrFromDepartment(permissions.BasePermission):
    def has_object_permission(self, request:Request, view:View, ticket:Ticket):
        ...