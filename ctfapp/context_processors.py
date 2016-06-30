import json


def site_configuration_processor(request):
    with open('djangoctf/settings.json') as config_file:
        config = json.loads(config_file.read())
        ctf_name = config['ctf_name']
        ctf_domain = config['ctf_platform_domain']
        shell_host = "shell.example.com"
        if config['shell']['enabled']:
            shell_host = config['shell']['hostname']

    return {'ctf_name': ctf_name, 'ctf_domain': ctf_domain, 'shell_host': shell_host}
