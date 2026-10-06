from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User, Profile


class ProfileInLine(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileInLine]
