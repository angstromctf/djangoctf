from django.core.exceptions import PermissionDenied
from ctfapp.util.time import before_start, after_end

def team_required(invert=False):
    def decorator(view):
        def wrap(request, *args, **kwargs):
            if (request.user.userprofile.team is not None) == invert:
                raise PermissionDenied
            else:
                return view(request, *args, **kwargs)

        wrap.__name__ = view.__name__
        wrap.__dict__ = view.__dict__
        wrap.__doc__ = view.__doc__

        return wrap
    return decorator

def lock_before_contest(view):
    def wrap(request, *args, **kwargs):
        if before_start() and not request.user.is_staff:
            raise PermissionDenied
        else:
            return view(request, *args, **kwargs)

    wrap.__name__ = view.__name__
    wrap.__dict__ = view.__dict__
    wrap.__doc__ = view.__doc__

    return wrap