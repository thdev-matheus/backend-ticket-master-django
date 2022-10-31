from rest_framework import permissions
from rest_framework.views import Request, View

from tickets.models import Ticket

class IsOwnerOrFromDepartment(permissions.BasePermission):
    def has_object_permission(self, request:Request, view:View, ticket:Ticket):
        return(
            request.user == ticket.user
            or request.user.department == ticket.department
            or request.user.is_superuser
        )