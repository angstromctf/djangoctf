"""The administrator interface.

Registers models for administrator access.
"""

# Import
from django.contrib import admin
from .models import Module


# Register models
admin.site.register(Module)