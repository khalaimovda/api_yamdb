from rest_framework import permissions


class IsSuperuserOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user == obj.author
            or request.user.is_moderator
        )
