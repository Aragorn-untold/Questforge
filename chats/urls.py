from django.urls import path

from chats.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = "chats"


urlpatterns = [
    path("", MessageListView.as_view(), name="chats-message-list"),
    path("create/", MessageCreateView.as_view(), name="chats-message-create"),
    path("<int:pk>/update/", MessageUpdateView.as_view(), name="chats-message-update"),
    path("<int:pk>/delete/", MessageDeleteView.as_view(), name="chats-message-delete"),
]
