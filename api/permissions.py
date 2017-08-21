from rest_framework import permissions
from rest_framework import authentication
from rest_framework import exceptions
from .models import APIKey


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Creates a signature
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class HasAPIAccess(permissions.BasePermission):
    """
    This is a global api key, if not key in headers no schema will be shown
    """
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        return APIKey.objects.filter(key=api_key).exists()
