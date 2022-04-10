from rest_framework.permissions import BasePermission, SAFE_METHODS

from reviews.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (not request.user.is_anonymous
                and request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous
                and request.user.is_admin)


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous
                and (request.user == obj.author
                     or request.user.role == User.MODERATOR
                     or request.user.is_admin))
