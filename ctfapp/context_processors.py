from django.conf import settings


def site_configuration_processor(request):
    ctf_name = settings.CONFIG['ctf_name']
    ctf_domain = settings.CONFIG['ctf_platform_domain']
    shell_host = "shell.example.com"

    if settings.CONFIG['shell']['enabled']:
        shell_host = settings.CONFIG['shell']['hostname']

    return {'ctf_name': ctf_name, 'ctf_domain': ctf_domain, 'shell_host': shell_host}
