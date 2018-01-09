from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Profile, Problem, Submission, Team, User


# Some Django magic to associate Profiles with Users
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)


# Register the combined user models with Django
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register models
admin.site.register(Problem)
admin.site.register(Profile)
admin.site.register(Submission)
admin.site.register(Team)
