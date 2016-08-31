from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from core.models import Team, CorrectSubmission, Profile
from core.decorators import team_required
from core.utils.time import contest_start, contest_end, minutes

import logging
import json
from random import choice

logger = logging.getLogger(__name__)


# Creates a random team code
def create_code():
    return "".join([choice("0123456789abcdef") for x in range(20)])


# Generates a random shell username
def create_shell_username():
    return "team" + "".join([choice("0123456789") for x in range(5)])


# Generates a random shell password
def create_shell_password():
    return "".join([choice("0123456789abcdef") for x in range(12)])


# Generates a score progression for a team suitable for Chart.js
def score_progression(team):
    submissions = CorrectSubmission.objects.all().filter(team=team)

    # Add the origin
    data = [{"x": 0, "y": 0}]

    for sub in submissions:
        # Add each submission
        data.append({"x": minutes(sub.time - contest_start), "y": sub.new_score})

    # Add final score
    data.append({"x": minutes(min(timezone.now(), contest_end) - contest_start), "y": team.score})

    return {"label": team.name, "data": data}


@login_required
@team_required(invert=True)
@require_POST
def create_team(request):
    """Creates a team for the user and adds them to that team."""

    form = CreateTeamForm(request.POST)

    if form.is_valid():
        code = create_code()
        while Team.objects.filter(code=code).count() > 0:
            code = create_code()

        shell_username = create_shell_username()
        while Team.objects.filter(shell_username=shell_username).count() > 0:
            shell_username = create_shell_username()

        shell_password = create_shell_password()

        # Check if we need to set up a shell account for the team
        if settings.CONFIG['shell']['enabled']:
            import paramiko

            ssh_private_key_path = settings.CONFIG['shell']['ssh_key_path']
            shell_hostname = settings.CONFIG['shell']['hostname']

            # SSH to shell server and create the account
            private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_path)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=shell_hostname, username='root', pkey=private_key)
            createuser_command = "addctfuser " + shell_username + " " + shell_password
            stdin, stdout, stderr = ssh.exec_command(createuser_command)

            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')

            if stderr != "":
                logger.error("Error while creating shell account.\nstdout: {}\nstderr: {}".format(stdout_data, stderr_data))

        # Create the team
        team = Team(name=form.cleaned_data['name'],
                    school=form.cleaned_data['affiliation'],
                    shell_username=shell_username,
                    shell_password=shell_password,
                    code=code,
                    eligible=request.user.profile.eligible)
        team.save()

        # Add the user to that team
        request.user.profile.team = team
        request.user.profile.save()

        return redirect('account')

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'create_team': form,
        'address_form': TeamAddressForm()
    })


@login_required
@team_required(invert=True)
@require_POST
def join_team(request):
    """Adds the user to a pre-existing team."""

    form = JoinTeamForm(request.POST)

    if form.is_valid():
        team = Team.objects.get(code=form.cleaned_data['code'])
        team.eligible = team.eligible and request.user.profile.eligible

        team.save()

        request.user.profile.team = team
        request.user.profile.save()

        return redirect('account')

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': form,
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })


@login_required
@team_required
@require_POST
def submit_addr(request):
    """Adds a team's shipping information for prizes."""

    team = request.user.profile.team
    form = TeamAddressForm(request.POST)

    if form.is_valid() and not team.address_street:
        team.address_street = form.cleaned_data['street_address']
        team.address_street_line_2 = form.cleaned_data['street_address_line_2']
        team.address_zip = form.cleaned_data['zip_5']
        team.address_city = form.cleaned_data['city']
        team.address_state = form.cleaned_data['state']
        team.eligible2 = form.cleaned_data['eligible2']

        team.save()
    else:
        return render(request, 'account.html', {
            'user': request.user,
            'change_password': ChangePasswordForm(user=request.user),
            'join_team': JoinTeamForm(user=request.user),
            'create_team': CreateTeamForm(),
            'address_form': form
        })

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })


def profile(request, team_id):
    """Displays basic information and score progression for a given team."""

    team = get_object_or_404(Team, id=team_id)

    # Sort the problems this team has solved
    ordered_solves = CorrectSubmission.objects.filter(team=team).order_by("time")

    data = [score_progression(team)]

    return render(request, 'profile.html', {
        'team': team,
        'ordered_solves': ordered_solves,
        'data': json.dumps(data)
    })


def scoreboard(request):
    """Displays the scoreboard as a list of teams and graph."""

    all_teams = Team.objects.all()
    scoring_teams = Team.objects.filter(score__gt=0).order_by('-score', 'score_lastupdate')

    graph_size = min(5, Team.objects.filter(score__gt=0).count())

    datasets = []

    for x in range(graph_size):
        datasets.append(score_progression(scoring_teams[x]))

    return render(request, 'scoreboard.html', {
        'all_teams': all_teams,
        'scoring_teams': scoring_teams,
        'data': json.dumps(datasets)
    })