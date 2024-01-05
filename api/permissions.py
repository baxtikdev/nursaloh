from rest_framework.permissions import BasePermission

from common.users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.is_active and request.user.role == User.UserRole.ADMIN)

class IsClient(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(
            request.user and request.user.is_active and request.user.is_verified is True and request.user.role == User.UserRole.CLIENT)
