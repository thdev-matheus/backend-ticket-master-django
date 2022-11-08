from rest_framework import permissions
from rest_framework.views import Request, View


class IsAdm(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_authenticated and request.user.is_superuser

class IsAdmOrListOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method == "GET"
            and request.user.is_authenticated 
            or request.user.is_authenticated 
            and request.user.is_superuser
        )
