from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from core.models import Team
from core.decorators import team_required

import logging
from random import choice


# Creates a random team code
def create_code():
    return "".join([choice("0123456789abcdef") for x in range(20)])


# Generates a random shell username
def create_shell_username():
    return "team" + "".join([choice("0123456789") for x in range(5)])


# Generates a random shell password
def create_shell_password():
    return "".join([choice("0123456789abcdef") for x in range(12)])

logger = logging.getLogger(__name__)

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
