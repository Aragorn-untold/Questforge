from django.contrib import admin

from characters.models import Character


@admin.register(Character)
class AdminCharacter(admin.ModelAdmin):
    pass
