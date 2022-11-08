from departments.models import Department
from rest_framework import permissions
from rest_framework.views import Request, View
from tickets.models import Ticket


class IsOwnerOrFromDepartment(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, ticket: Ticket):
        return (
            request.user == ticket.owner
            or request.user.is_authenticated
            and request.user.support_department == ticket.support_department
            or request.user.is_superuser
        )


class OnlyAdmCanListAll(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.method == "POST" or request.user.is_superuser


class IsFromDepartment(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: View, department: Department
    ):
        return (
            request.user.is_authenticated
            and request.user.support_department == department
            or request.user.is_superuser
        )
