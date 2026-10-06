from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404

from campaigns.models import Campaign, CampaignNote


User = get_user_model()


class CampaignOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().creator_id == self.request.user.pk


class CampaignNoteMembershipMixin(LoginRequiredMixin, UserPassesTestMixin):
    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, pk=kwargs["campaign_pk"])
        return super().dispatch(request, *args, **kwargs)

    def user_is_campaign_member(self):
        return self.campaign.creator_id == self.request.user.pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.campaign
        profile_pk = self.request.GET.get("from_profile")
        context["return_profile_user"] = (
            User.objects.filter(pk=profile_pk).first()
            if profile_pk and profile_pk.isdigit()
            else None
        )
        return context

    def get_success_url(self):
        query = "tab=notes"
        profile_pk = self.request.GET.get("from_profile")
        if profile_pk and profile_pk.isdigit():
            query += f"&from_profile={profile_pk}"
        return f"{self.campaign.get_absolute_url()}?{query}#campaign-notes"
