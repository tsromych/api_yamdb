from rest_framework import permissions


class UsersPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username
