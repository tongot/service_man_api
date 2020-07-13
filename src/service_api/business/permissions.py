from rest_framework import permissions
from .models import Business


class IsTheirOrder(permissions.BasePermission):
    message = "u are not allowed"

    def has_object_permission(self, request, view, obj):
        business = Business.objects.filter(owner_id=request.user.id).first()
        print("business")
        if business != None:
            if obj.business == business:
                return True
            return False
        return False


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """used to check if request from owner or from other surffer"""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
