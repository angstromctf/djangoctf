from django.contrib import admin

from .models import Problem

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
	inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Problem)
admin.site.register(UserProfile)