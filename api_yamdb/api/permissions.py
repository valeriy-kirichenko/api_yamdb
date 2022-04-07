from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous
                and request.user.role == User.ADMIN
                or request.user.is_staff)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous
                and request.user.role == User.ADMIN
                or request.user.is_staff)


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return not request.user.is_anonymous()

        if request.method in ('PATCH', 'DELETE'):
            return (request.user == obj.author
                    or request.user.role == User.ADMIN
                    or request.user.role == User.MODERATOR
                    or request.user.is_staff)

        if request.method in SAFE_METHODS:
            return True
        return False
