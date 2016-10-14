from rest_framework import permissions
from api.utils import time


def not_permission(perm):
    class NotPermission(permissions.BasePermission):
        def __init__(self, *args, **kwargs):
            self.inst = perm(*args, **kwargs)
            self.message = 'Opposite of {' + self.inst.message + '}.'

        def has_permission(self, request, view):
            return not self.inst.has_permission(request, view)

        def __getattribute__(self, s):
            try:
                x = super(NotPermission,self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x

            return self.inst.__getattribute__(s)

    return NotPermission


class ContestStarted(permissions.BasePermission):
    message = 'Not accessible before contest.'

    def has_permission(self, request, view):
        return not time.before_start()


class ContestEnded(permissions.BasePermission):
    message = 'Not accessible after contest.'

    def has_permission(self, request, view):
        return time.after_end()


class HasTeam(permissions.BasePermission):
    message = 'Team required.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.team
