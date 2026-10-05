from django.contrib import admin
from django.urls import path, include

from core.core_home_view import home_view


urlpatterns = [
    path("", home_view, name="home"),
    path("hello-there/admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("campaigns/", include("campaigns.urls", namespace="campaigns")),
    path("items/", include("items.urls", namespace="items")),
    path("quests/", include("quests.urls", namespace="quests")),
    path("monsters/", include("monsters.urls", namespace="monsters")),
    path("tavern/", include("chats.urls", namespace="chats"))
]
