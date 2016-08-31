from docker import Client
from io import BytesIO
from os.path import relpath

def docker(data, problem, category, problem_path):
    name = "djangoctf/{}".format(category + '-' + problem)

    cli = Client()
    response = [line for line in cli.build(path=problem_path, rm=True, tag=name, quiet=True)]

    container = cli.create_container(name, ports=[80], host_config=cli.create_host_config(port_bindings={
        80: 5000
    }))
    cli.start(container=container.get('Id'))
    # #print(cli.logs(container=container.get('Id')).decode('utf-8'))
