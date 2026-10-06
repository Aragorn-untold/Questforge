from django.urls import path, include

from compendium.views import compendium_view

app_name = "compendium"

urlpatterns = [
    path("", compendium_view, name="compendium-page"),
    path("items/", include("compendium.items.urls", namespace="items")),
    path("quests/", include("compendium.quests.urls", namespace="quests")),
    path("monsters/", include("compendium.monsters.urls", namespace="monsters")),
    path("spells/", include("compendium.spells.urls", namespace="spells")),
]
