from docker import Client


def docker(data, problem, category, problem_path):
    cli = Client()

    name = category + '-' + problem

    try:
        info = cli.inspect_image(name)
    except:
        pass

    if 'info' in locals():
        containers = cli.containers(filters={
            'ancestor': name
        })

        for container in containers:
            cli.remove_container(container['Id'], force=True)

        cli.remove_image(info['Id'])

    response = [line for line in cli.build(path=problem_path, rm=True, tag=name, quiet=True)]

    ports = []
    bindings = {}

    for container, host in data['deploy']['ports']:
        ports.append(container)
        bindings[container] = host

    container = cli.create_container(name, ports=ports, host_config=cli.create_host_config(port_bindings=bindings))
    cli.start(container=container['Id'])
