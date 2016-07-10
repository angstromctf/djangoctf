"""The administrator interface.

Registers models for administrator access.
"""

# Import
from django.contrib import admin
from .models import Node, Category, Module


# Register models
admin.site.register(Node)
admin.site.register(Category)
admin.site.register(Module)