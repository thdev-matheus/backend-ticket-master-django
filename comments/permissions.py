from rest_framework import permissions
from rest_framework.views import Request, View

from .models import Comment

class IsOwnerOrFromComment(permissions.BasePermission):
    def has_object_permission(self, request:Request, view:View, comment:Comment):
        return(
            request.user.id == comment.user_id
            or request.user.is_superuser
        )