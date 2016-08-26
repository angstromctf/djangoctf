from django.shortcuts import render, get_object_or_404, redirect

from .models import Module


def index(request):
    """Landing page for the learning platform, redirects to the first module."""

    # Find module with no prerequisites (this is defined as the first module)
    root = Module.objects.get(prereqs=None, parent=None)

    return redirect('learn:module', root.name)


def module(request, module_name):
    """Displays a given learning module's contents, along with navigation information."""

    module = get_object_or_404(Module.objects, name=module_name)

    # Find module with no prerequisites as the first/root module
    root = Module.objects.get(prereqs=None, parent=None)

    # Now we try to find the "next" module after this one: not necessarily the same as module.next
    # module.next represents the next sibling of module in the tree
    # next_module represents the next module we want the user to navigate to
    next_module = None

    # If this module has a child, then we want to visit the child next
    if module.first_child:
        next_module = module.first_child

    # Otherwise, scan up the module tree looking for a node with a next sibling
    current = module

    while current and next_module is None:
        if current.next:
            next_module = current.next
            break

        current = current.parent

    return render(request, "module.html", {
        'module': module,
        'root': root,
        'next': next_module
    })