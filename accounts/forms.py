from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Profile


class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about yourself"}),
    )
    gender = forms.ChoiceField(choices=Profile.GenderChoice.choices)
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name")

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
        self.profile = self.profile or getattr(self.instance, "profile", None)
        if self.profile:
            self.fields["bio"].initial = self.profile.bio
            self.fields["gender"].initial = self.profile.gender
            self.fields["birthday"].initial = self.profile.birthday

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile = self.profile or Profile(user=user)
            profile.bio = self.cleaned_data["bio"]
            profile.gender = self.cleaned_data["gender"]
            profile.birthday = self.cleaned_data["birthday"]
            profile.save()
            self.profile = profile
        return user


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Your hero’s name",
            "email": "youremail@email.com",
            "password1": "Create a password",
            "password2": "Confirm your password",
        }
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control register-input"
            field.widget.attrs["placeholder"] = placeholders.get(name, "")
