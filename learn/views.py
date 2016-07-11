from django.shortcuts import render
from .models import Module


def module(request, module_name):
    module = Module.objects.get(name=module_name)

    return render(request, "module.html", {
        'module': module
    })