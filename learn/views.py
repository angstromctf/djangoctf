from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template, Context

from .models import Module

def index(request):
    root = Module.objects.get(prereqs=None)

    return redirect('learn:module', root.name)

def module(request, module_name):
    module = get_object_or_404(Module.objects, name=module_name)
    root = Module.objects.get(prereqs=None)

    template = Template(module.text)

    next = None

    if module.first_child:
        next = module.first_child

    current = module

    while current and next is None:
        if current.next:
            next = current.next
            break

        current = current.parent

    return render(request, "module.html", {
        'module': module,
        'root': root,
        'contents': template.render(Context()),
        'next': next
    })