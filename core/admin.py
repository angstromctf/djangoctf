"""The administrator interface.

Defines the user profile, user administrator, and registers models
for administrator access.
"""

# Import
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, CorrectSubmission, IncorrectSubmission, Problem, Team, Update, ProblemUpdate


# Define user models
class UserProfileInline(admin.StackedInline):
    """Standard user profile."""
    
    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(UserAdmin):
    """Administrator profile"""
    
    inlines = (UserProfileInline,)


# Register both users with Django
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register models
admin.site.register(Problem)
admin.site.register(UserProfile)
admin.site.register(CorrectSubmission)
admin.site.register(IncorrectSubmission)
admin.site.register(Team)
admin.site.register(Update)
admin.site.register(ProblemUpdate)