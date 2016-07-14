from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.decorators import team_required
from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from core.models import Profile


@login_required
@team_required
@require_POST
def submit_addr(request):
    user_team = request.user.profile.team
    team_member_list = Profile.objects.filter(team=user_team)
    form = TeamAddressForm(request.POST)

    if form.is_valid() and not user_team.address_street:
        address_line1 = form.cleaned_data['street_address']
        address_line2 = form.cleaned_data['street_address_line_2']
        address_zip = form.cleaned_data['zip_5']
        address_city = form.cleaned_data['city']
        address_state = form.cleaned_data['state']

        user_team = request.user.profile.team

        user_team.address_street = address_line1
        user_team.address_street_line_2 = address_line2
        user_team.address_zip = address_zip
        user_team.address_city = address_city
        user_team.address_state = address_state
        user_team.eligible2 = form.cleaned_data['eligible2']
        user = request.user.profile
        user.eligible = form.cleaned_data['eligible2']
        user.save()
        user_team.save()
    else:

        return render(request, 'account.html', {
            'user': request.user,
            'change_password': ChangePasswordForm(user=request.user),
            'join_team': JoinTeamForm(user=request.user),
            'team_member_list': team_member_list,
            'create_team': CreateTeamForm(),

            'address_form': form
        })

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'team_member_list': team_member_list,
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })
