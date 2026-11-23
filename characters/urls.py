from django.urls import path

from characters.views import (
    CharacterListView,
    CharacterDetailView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDeleteView,
)

app_name = "characters"

urlpatterns = [
    path("", CharacterListView.as_view(), name="character-list"),
    path("<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("create/", CharacterCreateView.as_view(), name="character-create"),
    path("<int:pk>/update/", CharacterUpdateView.as_view(), name="character-update"),
    path("<int:pk>/delete/", CharacterDeleteView.as_view(), name="character-delete"),
]
