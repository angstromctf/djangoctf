from django.core.management.base import BaseCommand

from learn.models import Module

import os
import json
import markdown2

class Command(BaseCommand):
    help = 'Update learning modules by reading from directory.'

    def add_arguments(self, parser):
        parser.add_argument('module-dir', type=str)

    def handle(self, *args, **options):
        modules = {}

        def parse(dir, name, parent):
            # Check if this is a valid module
            if os.path.exists(os.path.join(dir, 'module.json')):
                file = open(os.path.join(dir, 'module.json'))
                data = json.loads(file.read())
                file.close()

                # Check if this module already exists (whether we're updating or creating a module)
                if Module.objects.filter(name=name):
                    module = Module.objects.get(name=name)
                else:
                    module = Module(name=name)

                module.title = data['title']

                file = open(os.path.join(dir, 'contents.md'))
                module.text = markdown2.markdown(file.read())
                file.close()

                module.parent = parent

                module.save()

                modules[module] = data

                print('Successfully updated model %s.' % (module.name))
            elif name == '':
                module = None
            else:
                return

            for sub in os.listdir(dir):
                if sub != 'module.json' and sub != 'module.html' and os.path.isdir(os.path.join(dir, sub)):
                    parse(os.path.join(dir, sub), sub, module)

        parse(options['module-dir'], '', None)

        for module, data in modules.items():
            if 'prereqs' in data:
                module.prereqs.set(Module.objects.filter(name__in=data['prereqs']).all())
            else:
                module.prereqs.set(module.prevs.all())

            if 'next' in data:
                module.next = Module.objects.get(name=data['next'])

            if 'first_child' in data:
                module.first_child = Module.objects.get(name=data['first_child'])

            module.save()