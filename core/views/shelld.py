from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.decorators import lock_before_contest


@login_required
@lock_before_contest
def shelld(request):
    """Displays the online shell."""

    return render(request, "shelld.html")
