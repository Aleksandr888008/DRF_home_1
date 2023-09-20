from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Права доступа владельца"""

    message = 'Доступ ограничен! Вы не являетесь владельцем записи'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsModerator(BasePermission):
    """Права доступа модератора"""
    message = 'Доступ ограничен! Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
