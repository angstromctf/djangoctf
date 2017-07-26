import typing
from rest_framework import permissions

from api import utils


class AntiPermission(permissions.BasePermission):
    """A permission that negates another permission."""

    def __init__(self, permission: typing.Type[permissions.BasePermission], *args, **kwargs):
        """Initialize a new anti-permission."""

        self.__permission = permission(*args, **kwargs)
        if hasattr(self.__permission, "message"):
            self.message = "Opposite of {" + self.__permission.message + "}."

    def has_permission(self, request, view):
        """Check if a permission is granted."""

        return not self.__permission.has_permission(request, view)

    def __getattribute__(self, key):
        """Get an attribute of the anti-permission."""

        try:
            value = super().__getattribute__(key)
        except AttributeError:
            return self.__permission.__getattribute__(key)
        else:
            return value


def not_permission(perm):

    return AntiPermission(perm)


class ContestStarted(permissions.BasePermission):
    message = 'Not accessible before contest.'

    def has_permission(self, request, view):
        return not utils.before_start()


class ContestEnded(permissions.BasePermission):
    message = 'Not accessible after contest.'

    def has_permission(self, request, view):
        return utils.after_end()


class HasTeam(permissions.BasePermission):
    message = 'Team required.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.team
