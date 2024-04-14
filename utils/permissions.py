from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User


class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to access it.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.user_type == User.UserType.ADMIN)

    def has_object_permission(self, request, view, obj):
        return request.user.user_type == User.UserType.ADMIN or (
            obj == request.user and request.method in ["GET", "PATCH"]
        )


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.user_type == User.UserType.ADMIN)


class CustomPermission(IsAuthenticated):
    """
    Custom permission that requires the user to be authenticated and have a specific attribute.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.has_attribute
