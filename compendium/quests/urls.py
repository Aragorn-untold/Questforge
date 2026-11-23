from django.urls import path

from compendium.quests.views import QuestListView, QuestDetailView


app_name = "quests"

urlpatterns = [
    path("", QuestListView.as_view(), name="quest-list"),
    path("<int:pk>/", QuestDetailView.as_view(), name="quest-detail")
]
