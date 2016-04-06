from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from ctfapp.utils.time import before_start

from functools import wraps

"""
Various authentication checks as decorators.
"""


def team_required(function=None, invert=False):
    def decorator(view):
        @wraps(view, assigned=available_attrs(view))
        def wrap(request, *args, **kwargs):
            if (request.user.userprofile.team is not None) == invert:
                raise PermissionDenied
            else:
                return view(request, *args, **kwargs)
        return wrap

    if function:
        return decorator(function)
    else:
        return decorator


def lock_before_contest(view):
    @wraps(view, assigned=available_attrs(view))
    def wrap(request, *args, **kwargs):
        if before_start() and not request.user.is_staff:
            return render(request, 'denied.html', {})
        else:
            return view(request, *args, **kwargs)

    return wrap
