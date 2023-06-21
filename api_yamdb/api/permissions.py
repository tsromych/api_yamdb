from rest_framework import permissions


#
class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAuthorOrModeratorOrAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 # or request.user.is_moderator
                 or obj.author == request.user)
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )


# class IsOwner(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated)

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if not request.user.is_authenticated:
#             return False
#         return (obj.author == request.user
#                 or request.user.is_moderator
#                 or request.user.is_admin)


# class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_moderator
#             or request.user.is_admin
#             or obj.author == request.user
#         )
