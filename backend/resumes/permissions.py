from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read-only allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # write only if current user owns the resume
        return obj.owner == request.user
