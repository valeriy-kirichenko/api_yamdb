from rest_framework import permissions

from users.models import User


class IsAdmin(permissions.BasePermission):
    """Разрешение для Админа и Суперпользователя."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (
                request.user.role == User.ADMIN or request.user.is_superuser))
