from django.core.exceptions import PermissionDenied

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