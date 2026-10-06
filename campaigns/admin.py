from django.contrib import admin

from campaigns.models import Campaign


@admin.register(Campaign)
class AdminCampaign(admin.ModelAdmin):
    pass
