from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import UserProfileUpdateForm, UserRegisterForm
from accounts.services.user_service import UserService
from accounts.services.user_activation_token_service import activation_token_service
from characters.models import Character

User = get_user_model()

class UserListView(LoginRequiredMixin, generic.ListView):
    model = User


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    context_object_name = "profile_user"

    def get_queryset(self):
        return User.objects.select_related("profile").prefetch_related(
            "campaigns",
            Prefetch(
                "characters",
                queryset=Character.objects.select_related(
                    "campaign", "race", "character_class"
                ),
                to_attr="profile_characters",
            ),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_profile"] = getattr(self.object, "profile", None)
        characters = self.object.profile_characters
        participating_campaigns = {
            character.campaign_id: character.campaign for character in characters
        }
        context["created_campaigns"] = self.object.campaigns.all()
        context["participating_campaigns"] = sorted(
            participating_campaigns.values(),
            key=lambda campaign: campaign.created_at,
            reverse=True,
        )
        context["created_characters"] = characters
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = "accounts/user_form.html"

    def get_queryset(self):
        return User.objects.select_related("profile")

    def test_func(self):
        return self.get_object() == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["profile"] = getattr(self.object, "profile", None)
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()


class UserRegisterView(generic.FormView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    user_service = UserService(token_service=activation_token_service)
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:user-detail", pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        url = self.request.build_absolute_uri("/")
        self.user_service.register_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
            url=url
        )
        messages.success(
            self.request,
            "User created successfully, check your email to activate your account"
        )
        return super().form_valid(form)


class UserActivationView(generic.View):
    def get(self, request, uid, token):
        print(uid, token)
        print("we need to activate the user")
