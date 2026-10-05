from django.views import generic

from campaigns.forms import CampaignNoteForm
from campaigns.mixin import CampaignNoteMembershipMixin
from campaigns.models import CampaignNote


class CampaignNoteCreateView(CampaignNoteMembershipMixin, generic.CreateView):
    model = CampaignNote
    form_class = CampaignNoteForm
    template_name = "campaigns/campaignnote_form.html"

    def test_func(self):
        return self.user_is_campaign_member()

    def form_valid(self, form):
        form.instance.campaign = self.campaign
        form.instance.user = self.request.user
        return super().form_valid(form)


class CampaignNoteUpdateView(CampaignNoteMembershipMixin, generic.UpdateView):
    model = CampaignNote
    form_class = CampaignNoteForm
    template_name = "campaigns/campaignnote_form.html"

    def get_queryset(self):
        return CampaignNote.objects.filter(campaign=self.campaign).select_related(
            "campaign", "user"
        )

    def test_func(self):
        note = self.get_object()
        return self.user_is_campaign_member() and (
            note.user_id == self.request.user.pk
            or self.campaign.creator_id == self.request.user.pk
        )


class CampaignNoteDeleteView(CampaignNoteMembershipMixin, generic.DeleteView):
    model = CampaignNote
    template_name = "campaigns/campaignnote_confirm_delete.html"

    def get_queryset(self):
        return CampaignNote.objects.filter(campaign=self.campaign).select_related(
            "campaign", "user"
        )

    def test_func(self):
        note = self.get_object()
        return self.user_is_campaign_member() and (
            note.user_id == self.request.user.pk
            or self.campaign.creator_id == self.request.user.pk
        )
