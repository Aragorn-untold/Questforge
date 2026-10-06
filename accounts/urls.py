from django.urls import path, include

from accounts.views import UserDetailView, UserListView, UserUpdateView, UserRegisterView, UserActivationView

app_name = "accounts"


urlpatterns = [
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/update", UserUpdateView.as_view(), name="user-update"),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path(
        "activate/<str:uid>/<str:token>/",
        UserActivationView.as_view(),
        name="activate"
    ),
    path("", include("django.contrib.auth.urls")),
]
