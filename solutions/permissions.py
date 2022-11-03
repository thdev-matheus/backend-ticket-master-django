from rest_framework import permissions
from rest_framework.views import Request, View

from tickets.models import Ticket

class IsAdmOrFromTicketDepartmentOrOwner(permissions.BasePermission):
    def has_object_permission(self, request:Request, view:View, ticket:Ticket):       
        return(
            request.user.is_superuser
            or request.user == ticket.support
            or request.user.department == ticket.support_department
            or request.user == ticket.user
        )