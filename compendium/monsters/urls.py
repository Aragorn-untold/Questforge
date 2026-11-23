from django.urls import path

from compendium.monsters.views import MonsterListView, MonsterDetailView

app_name = "monsters"

urlpatterns = [
    path("", MonsterListView.as_view(), name="monster-list"),
    path("<int:pk>/", MonsterDetailView.as_view(), name="monster-detail"),
]