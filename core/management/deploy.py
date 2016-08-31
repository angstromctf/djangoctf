from docker import Client
from io import BytesIO
from os.path import relpath

def docker(data, problem, category, problem_path):
    cli = Client()

    name = category + '-' + problem

    try:
        info = cli.inspect_image(name)
    except:
        pass

    if 'info' in locals():
        containers = cli.containers(filters={
            'ancestor': 'web-amoebananas'
        })

        for container in containers:
            cli.remove_container(container['Id'], force=True)

        cli.remove_image(info['Id'])

    response = [line for line in cli.build(path=problem_path, rm=True, tag=name, quiet=True)]

    container = cli.create_container(name, ports=[80], host_config=cli.create_host_config(port_bindings={
        80: 5000
    }))
    cli.start(container=container['Id'])
