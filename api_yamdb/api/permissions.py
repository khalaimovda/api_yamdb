from rest_framework import permissions


class IsSuperuserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsSuperuserOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorOrModeratorOrAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )
