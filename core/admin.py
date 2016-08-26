from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from core.models import Profile, CorrectSubmission, IncorrectSubmission, Problem, Team, ProblemUpdate


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
admin.site.register(CorrectSubmission)
admin.site.register(IncorrectSubmission)
admin.site.register(Team)
admin.site.register(ProblemUpdate)