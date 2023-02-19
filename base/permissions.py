from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    message = "You are not a superuser. Action restricted."
    def has_permission(self, request, view) -> bool:
        return request.user.is_superuser


class IsStaff(BasePermission):
    message = "You are not an active staff. Action restricted."
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_active

class IsActiveMember(BasePermission):
    message = "You are not an active staff. Action restricted."
    def has_permission(self, request, view) -> bool:
        return request.user.is_active 

