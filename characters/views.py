from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from campaigns.models import Campaign
from characters.models import Character

User = get_user_model()

class CharacterListView(generic.ListView):
    model = Character

    def get_queryset(self):
        return Character.objects.filter(campaign_id=self.kwargs["campaign_pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campaign = get_object_or_404(Campaign, pk=self.kwargs["campaign_pk"])
        context["campaign"] = campaign
        profile_pk = self.request.GET.get("from_profile")
        context["return_profile_user"] = (
            User.objects.filter(pk=profile_pk).first()
            if profile_pk and profile_pk.isdigit() else None
        )
        context["user_character"] = (
            campaign.characters.filter(player=self.request.user).first()
            if self.request.user.is_authenticated else None
        )
        return context


class CharacterDetailView(generic.DetailView):
    model = Character
    queryset = Character.objects.select_related(
        "campaign", "player", "race", "character_class"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.request.GET.get("from_profile")
        context["return_profile_user"] = (
            User.objects.filter(pk=profile_pk).first()
            if profile_pk and profile_pk.isdigit() else None
        )
        return context


class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
    model = Character
    fields = ("name", "race", "character_class", "gender", "bio")

    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, pk=kwargs["campaign_pk"])
        if self.campaign.is_active == Campaign.ActiveChoice.ENDED:
            return redirect(self.campaign.get_absolute_url())
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if Character.objects.filter(campaign=self.campaign, player=request.user).exists():
            return redirect(self.campaign.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.campaign = self.campaign
        form.instance.player = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.campaign
        return context

    def get_success_url(self):
        return self.campaign.get_absolute_url()


class CharacterUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Character
    fields = ("name", "race", "character_class", "gender", "bio")

    def get_queryset(self):
        return Character.objects.filter(player=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.object.campaign
        return context

    def get_success_url(self):
        return self.object.campaign.get_absolute_url()


class CharacterDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Character
    template_name = "characters/character_confirm_delete.html"

    def get_queryset(self):
        return Character.objects.filter(
            campaign_id=self.kwargs["campaign_pk"], player=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.object.campaign
        return context

    def get_success_url(self):
        return self.object.campaign.get_absolute_url()
