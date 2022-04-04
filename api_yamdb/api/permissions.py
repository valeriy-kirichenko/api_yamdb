from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.role == 'admin'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous
                and request.user.role == 'admin')


class IsAuthorOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return (obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator')
