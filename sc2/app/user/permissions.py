from rest_framework import permissions


class IsOwnerOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
