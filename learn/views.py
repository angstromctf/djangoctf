from django.shortcuts import render, get_object_or_404
from django.template import Template, Context

from .models import Module


def module(request, module_name):
    module = get_object_or_404(Module.objects, name=module_name)
    root = Module.objects.get(prereqs=None)

    template = Template(module.text)

    return render(request, "module.html", {
        'module': module,
        'root': root,
        'contents': template.render(Context())
    })