from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, AllowAny


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admin users to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin
        if request.user and request.user.is_staff:
            return True

        # Check if the user is the owner of the object
        return obj.owner == request.user


class CustomPermission(IsAuthenticated):
    """
    Custom permission that requires the user to be authenticated and have a specific attribute.
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.has_attribute
