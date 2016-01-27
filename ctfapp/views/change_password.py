import json

from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def change_password(request: HttpRequest):
    """
    View for changing a password through AJAX.  Login is required.
    """

    alert_type = "danger"
    alert_class = "glyphicon glyphicon-remove-sign"

    password = request.POST["old"]

    user = authenticate(username=request.user.get_username(), password=password)

    if user:
        if request.POST["new"] == request.POST["confirm"]:
            new = request.POST["new"]

            if new:
                user.set_password(new)
                user.save()

                login(request, user)

                alert = "<strong>Yay!</strong> Password change successful!"
                alert_type = "success"
                alert_class = "glyphicon glyphicon-ok-sign"
            else:
                alert = "<strong>Oops!</strong> Password may not be empty."
        else:
            alert = "<strong>Oops!</strong> Passwords must match."
    else:
        alert = "<strong>Oops!</strong> Incorrect password."

    response_data = {"alert": alert, "alert_type": alert_type, "alert_class": alert_class}
    return HttpResponse(json.dumps(response_data), content_type="application/json")