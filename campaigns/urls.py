from django.urls import path, include

from campaigns.views import (
    CampaignListView,
    CampaignCreateView,
    CampaignDetailView,
    CampaignUpdateView,
    CampaignDeleteView, CampaignItemCreationView, CampaignQuestCreationView, CampaignMonsterCreationView,
)
from campaigns.note_views import (
    CampaignNoteCreateView,
    CampaignNoteDeleteView,
    CampaignNoteUpdateView,
)

app_name = "campaigns"

urlpatterns = [
    path("", CampaignListView.as_view(), name="campaign-list"),
    path("create/", CampaignCreateView.as_view(), name="campaign-create"),
    path("<int:pk>/", CampaignDetailView.as_view(), name="campaign-detail"),
    path("<int:pk>/update/", CampaignUpdateView.as_view(), name="campaign-update"),
    path("<int:pk>/delete/", CampaignDeleteView.as_view(), name="campaign-delete"),
    path(
        "<int:campaign_pk>/notes/create/",
        CampaignNoteCreateView.as_view(),
        name="campaign-note-create",
    ),
    path(
        "<int:campaign_pk>/notes/<int:pk>/update/",
        CampaignNoteUpdateView.as_view(),
        name="campaign-note-update",
    ),
    path(
        "<int:campaign_pk>/notes/<int:pk>/delete/",
        CampaignNoteDeleteView.as_view(),
        name="campaign-note-delete",
    ),
    path(
        "<int:campaign_pk>/characters/",
        include("characters.urls", namespace="characters"),
    ),
    path(
        "<int:campaign_pk>/items/",
        CampaignItemCreationView.as_view(),
        name="campaign-item-list"
    ),
    path(
        "<int:campaign_pk>/items/from-item/<int:item_pk>/",
        CampaignItemCreationView.as_view(),
        name="campaign-item-create-from-item",
    ),
    path(
        "<int:campaign_pk>/quests/",
        CampaignQuestCreationView.as_view(),
        name="campaign-quest-list"
    ),
    path(
        "<int:campaign_pk>/quests/from-quest/<int:quest_pk>/",
        CampaignQuestCreationView.as_view(),
        name="campaign-quest-create-from-item"
    ),
    path(
        "<int:campaign_pk>/monsters/",
        CampaignMonsterCreationView.as_view(),
        name="campaign-monster-list"
    ),
    path(
        "<int:campaign_pk>/monsters/from_monster/<int:monster_pk>/",
        CampaignMonsterCreationView.as_view(),
        name="campaign-monster-create-from-monster"
    )
]
