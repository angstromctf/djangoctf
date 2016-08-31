from docker import Client


def docker(data, problem, category, problem_path):
    cli = Client()

    name = category + '-' + problem

    try:
        # Check if this image already exists (it'll throw an error if it doesn't)
        info = cli.inspect_image(name)
    except:
        pass

    if 'info' in locals():
        # Find all containers from this image
        containers = cli.containers(filters={
            'ancestor': name
        })

        # Destroy them and the image
        for container in containers:
            cli.remove_container(container['Id'], force=True)

        cli.remove_image(info['Id'])

    # Build a new image in the problem's directory
    response = cli.build(path=problem_path, rm=True, tag=name, quiet=True)

    # Compile a list of ports and a map of port bindings
    ports = []
    bindings = {}

    for container, host in data['deploy']['ports']:
        ports.append(container)
        bindings[container] = host

    # Create the container from the specified image, with port bindings
    container = cli.create_container(name, ports=ports, host_config=cli.create_host_config(port_bindings=bindings))

    # Start the container
    cli.start(container=container['Id'])
