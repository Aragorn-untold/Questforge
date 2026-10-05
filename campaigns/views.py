from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from campaigns.mixin import CampaignOwnerMixin
from campaigns.models import Campaign, CampaignNote
from campaigns.forms import CampaignNoteForm, CampaignUpdateForm, CampaignSearchForm
from items.forms import CampaignItemForm
from items.models import CampaignItem, Item
from monsters.forms import CampaignMonsterForm
from monsters.models import CampaignMonster, Monster
from quests.forms import CampaignQuestForm
from quests.models import CampaignQuest, Quest

User = get_user_model()

class CampaignListView(generic.ListView):
    model = Campaign
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign_search_form"] = CampaignSearchForm(initial={"title": self.request.GET.get("title", "")})
        context["clear"] = context.get("campaign_search_form", "")["title"].value() or None
        return context

    def get_queryset(self):
        queryset = Campaign.objects.all()
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class CampaignDetailView(generic.DetailView):
    model = Campaign
    queryset = Campaign.objects.select_related("creator")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_campaign_owner = self.request.user.is_authenticated and (
            self.object.creator_id == self.request.user.pk
        )
        profile_pk = self.request.GET.get("from_profile")
        context["return_profile_user"] = (
            User.objects.filter(pk=profile_pk).first()
            if profile_pk and profile_pk.isdigit() else None
        )
        user_character = (
            self.object.characters.filter(player=self.request.user).first()
            if self.request.user.is_authenticated else None
        )
        can_access_notes = is_campaign_owner
        context["is_campaign_owner"] = is_campaign_owner
        context["user_character"] = user_character
        context["characters"] = self.object.characters.select_related(
            "player", "race", "character_class"
        )
        context["can_access_notes"] = can_access_notes
        context["campaign_notes"] = (
            self.object.notes.select_related("user").order_by("-created_at")
            if can_access_notes else CampaignNote.objects.none()
        )
        context["campaign_note_form"] = CampaignNoteForm() if can_access_notes else None
        if is_campaign_owner:
            context["campaign_items"] = self.object.items.select_related("base_item")
            context["campaign_quests"] = self.object.quests.select_related("base_quest")
            context["campaign_monsters"] = self.object.monsters.select_related("base_monster")
        return context


class CampaignCreateView(LoginRequiredMixin, generic.CreateView):
    model = Campaign
    fields = ("title", "description")
    success_url = reverse_lazy("campaigns:campaign-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CampaignUpdateView(CampaignOwnerMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignUpdateForm

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class CampaignDeleteView(CampaignOwnerMixin, generic.DeleteView):
    model = Campaign
    success_url = reverse_lazy("campaigns:campaign-list")
    template_name = "campaigns/campaign_confirm_delete.html"


class CampaignItemCreationView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = CampaignItem
    form_class = CampaignItemForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, pk=kwargs["campaign_pk"])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.campaign.creator_id == self.request.user.pk

    def get_initial(self):
        initial = super().get_initial()
        item_pk = self.kwargs.get("item_pk")
        if item_pk:
            item = get_object_or_404(Item, pk=item_pk)
            initial.update(item.to_campaign_item())
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.campaign
        context["campaign_items"] = self.campaign.items.select_related("base_item")
        context["base_items_data"] = list(
            Item.objects.values(
                "id", "name", "type", "rarity", "description", "damage",
                "protection", "effect", "weight", "price"
            )
        )
        return context

    def form_valid(self, form):
        form.instance.campaign = self.campaign
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.campaign.get_absolute_url()


class CampaignQuestCreationView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = CampaignQuest
    form_class = CampaignQuestForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, pk=kwargs["campaign_pk"])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.campaign.creator_id == self.request.user.id

    def get_initial(self):
        initial = super().get_initial()
        base_quest_pk = self.kwargs.get("quest_pk")
        if base_quest_pk:
            quest = get_object_or_404(Quest, pk=base_quest_pk)
            initial.update(quest.to_campaign_quest())
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.campaign
        context["campaign_quests"] = self.campaign.quests.select_related("base_quest")
        context["base_quests_data"] = list(
            Quest.objects.values(
                "id", "title", "description", "reward_description",
                "difficulty_rating", "level_recommendation"
            )
        )
        return context

    def form_valid(self, form):
        form.instance.campaign = self.campaign
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.campaign.get_absolute_url()


class CampaignMonsterCreationView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = CampaignMonster
    form_class = CampaignMonsterForm

    def dispatch(self, request, *args, **kwargs):
        self.campaign = get_object_or_404(Campaign, pk=kwargs["campaign_pk"])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.campaign.creator_id == self.request.user.id

    def get_initial(self):
        initial = super().get_initial()
        base_monster_pk = self.kwargs.get("monster_pk")
        if base_monster_pk:
            monster = get_object_or_404(Monster, pk=base_monster_pk)
            initial.update(monster.to_campaign_monster())
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["campaign"] = self.campaign
        context["campaign_monsters"] = self.campaign.monsters.select_related("base_monster")
        context["base_monster_data"] = list(
            Monster.objects.values(
                "id", "name",
                "type", "alignment",
                "challenge_rating",
                "hit_points", "armor_class",
                "abilities"
            )
        )
        return context

    def form_valid(self, form):
        form.instance.campaign = self.campaign
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.campaign.get_absolute_url()
