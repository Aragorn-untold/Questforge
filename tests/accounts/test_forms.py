from datetime import date

from django.test import TestCase

from accounts.forms import UserProfileUpdateForm, UserRegisterForm
from accounts.models import Profile
from tests.helpers import create_user


class UserProfileUpdateFormTests(TestCase):
    def test_initial_values_are_loaded_from_existing_profile(self):
        user = create_user("profile-owner")
        user.profile.bio = "A seasoned explorer."
        user.profile.gender = Profile.GenderChoice.FEMALE
        user.profile.birthday = date(1995, 4, 12)
        user.profile.save()

        form = UserProfileUpdateForm(instance=user, profile=user.profile)

        self.assertEqual(form["bio"].value(), "A seasoned explorer.")
        self.assertEqual(form["gender"].value(), Profile.GenderChoice.FEMALE)
        self.assertEqual(form["birthday"].value(), date(1995, 4, 12))

    def test_save_updates_user_and_profile_fields_together(self):
        user = create_user("profile-owner")
        form = UserProfileUpdateForm(
            data={
                "first_name": "Ariadne",
                "last_name": "Vale",
                "bio": "Maps forgotten roads.",
                "gender": Profile.GenderChoice.OTHER,
                "birthday": "1994-08-23",
            },
            instance=user,
            profile=user.profile,
        )

        self.assertTrue(form.is_valid(), form.errors)
        saved_user = form.save()
        saved_user.refresh_from_db()
        saved_user.profile.refresh_from_db()
        self.assertEqual((saved_user.first_name, saved_user.last_name), ("Ariadne", "Vale"))
        self.assertEqual(saved_user.profile.bio, "Maps forgotten roads.")
        self.assertEqual(saved_user.profile.birthday, date(1994, 8, 23))

    def test_save_creates_a_profile_if_user_does_not_have_one(self):
        user = create_user("missing-profile")
        user.profile.delete()
        user._state.fields_cache.pop("profile", None)
        form = UserProfileUpdateForm(
            data={
                "first_name": "New",
                "last_name": "Profile",
                "bio": "Created through the edit form.",
                "gender": Profile.GenderChoice.MALE,
                "birthday": "",
            },
            instance=user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(user.profile.bio, "Created through the edit form.")


class UserRegisterFormTests(TestCase):
    def test_registration_form_exposes_email(self):
        form = UserRegisterForm()

        self.assertIn("email", form.fields)

    def test_registration_fields_have_design_classes_and_placeholders(self):
        form = UserRegisterForm()

        for field in form.fields.values():
            self.assertIn("register-input", field.widget.attrs["class"])
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Your hero’s name",
        )
        self.assertEqual(
            form.fields["email"].widget.attrs["placeholder"],
            "youremail@email.com",
        )
