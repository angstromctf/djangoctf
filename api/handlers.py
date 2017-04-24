from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Team

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, Team)
def create_team(team, **kwargs):
    # When a team is created, SSH into the shell server and make it a shell account
    if 'created' in kwargs and kwargs['created'] and settings.SHELL_ENABLED:
        import paramiko

        private_key = paramiko.RSAKey.from_private_key_file(settings.SHELL_PRIVATE_KEY)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=settings.SHELL_HOSTNAME, username='root', pkey=private_key)

        command = "/root/addctfuser " + team.shell_username + " " + team.shell_password
        stdin, stdout, stderr = ssh.exec_command(command)

        stdout_data = stdout.read().decode('utf-8')
        stderr_data = stderr.read().decode('utf-8')

        if stderr != "":
            logger.error("Error while creating shell account.\nstdout: {}\nstderr: {}".format(stdout_data, stderr_data))