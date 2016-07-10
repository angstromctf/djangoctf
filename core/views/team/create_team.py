from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from core.models import Team
from core.decorators import team_required

import logging
from random import choice


# Create random team code
def create_code():
    return "".join([choice("0123456789abcdef") for x in range(20)])


# Generate shell username
def create_shell_username():
    return "team" + "".join([choice("0123456789") for x in range(5)])


def create_shell_password():
    return "".join([choice("0123456789abcdef") for x in range(12)])

logger = logging.getLogger(__name__)

# Handle the HTTP request
@login_required
@team_required(invert=True)
@require_POST
def create_team(request: HttpRequest):
    """Create the account page."""

    shell_enabled = settings.CONFIG['shell']['enabled']

    if shell_enabled:
        ssh_priv_key_path = settings.CONFIG['shell']['ssh_key_path']
        shell_hostname = settings.CONFIG['shell']['hostname']

    form = CreateTeamForm(request.POST)

    if form.is_valid():
        code = create_code()
        while Team.objects.filter(code=code).count() > 0:
            code = create_code()

        shell_username = create_shell_username()
        while Team.objects.filter(shell_username=shell_username).count() > 0:
            shell_username = create_shell_username()

        shell_password = create_shell_password()

        if shell_enabled:
            import paramiko

            # SSH to shell server and create the account
            pkey = paramiko.RSAKey.from_private_key_file(ssh_priv_key_path)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=shell_hostname, username='root', pkey=pkey)
            createuser_command = "addctfuser " + shell_username + " " + shell_password
            stdin, stdout, stderr = ssh.exec_command(createuser_command)

            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')

            if stderr != '':
                logger.error("""Error while creating shell account.
                stdout: """ + stdout_data + """
                stderr: """ + stderr_data)

        team = Team(name=form.cleaned_data['name'],
                    user_count=1,
                    school=form.cleaned_data['affiliation'],
                    shell_username=shell_username,
                    shell_password=shell_password,
                    code=code,
                    eligible=request.user.userprofile.eligible)

        team.save()
        team.users.add(request.user)

        request.user.userprofile.team = team
        request.user.userprofile.save()

        return redirect('/account/')

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(user=request.user),
                                            'join_team': JoinTeamForm(user=request.user),
                                            'create_team': form})
