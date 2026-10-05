from django.urls import path

from items.views import ItemListView, ItemDetailView

app_name = "items"

urlpatterns = [
    path("", ItemListView.as_view(), name="item-list"),
    path("<int:pk>/", ItemDetailView.as_view(), name="item-detail")
]
