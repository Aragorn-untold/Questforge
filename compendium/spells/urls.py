from django.urls import path

from compendium.spells.views import SpellListView, SpellDetailView

app_name = "spells"

urlpatterns = [
    path("", SpellListView.as_view(), name="spell-list"),
    path("<int:pk>/", SpellDetailView.as_view(), name="spell-detail")
]
