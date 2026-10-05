from datetime import date

from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from tests.helpers import create_campaign, create_character, create_user


class UserProfileViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("profile-owner")
        self.other = create_user("profile-other")
        self.detail_url = reverse("accounts:user-detail", args=[self.owner.pk])
        self.update_url = reverse("accounts:user-update", args=[self.owner.pk])

    def test_profile_email_is_visible_only_to_its_owner(self):
        self.client.force_login(self.other)
        other_response = self.client.get(self.detail_url)
        self.assertEqual(other_response.status_code, 200)
        self.assertNotContains(other_response, self.owner.email)

        self.client.force_login(self.owner)
        owner_response = self.client.get(self.detail_url)
        self.assertContains(owner_response, self.owner.email)

    def test_only_profile_owner_can_open_edit_page(self):
        self.client.force_login(self.other)

        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 403)

    def test_profile_edit_updates_user_and_profile_then_returns_to_profile(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.update_url,
            {
                "first_name": "Updated",
                "last_name": "Name",
                "bio": "Changed bio.",
                "gender": Profile.GenderChoice.FEMALE,
                "birthday": "1992-11-03",
            },
        )

        self.assertRedirects(response, self.detail_url)
        self.owner.refresh_from_db()
        self.owner.profile.refresh_from_db()
        self.assertEqual(self.owner.first_name, "Updated")
        self.assertEqual(self.owner.last_name, "Name")
        self.assertEqual(self.owner.profile.bio, "Changed bio.")
        self.assertEqual(self.owner.profile.birthday, date(1992, 11, 3))

    def test_profile_lists_authored_joined_campaigns_and_characters(self):
        campaign = create_campaign(creator=self.owner, title="Created world")
        joined_campaign = create_campaign(creator=self.other, title="Joined world")
        character = create_character(joined_campaign, self.owner, name="Profile Hero")
        self.client.force_login(self.owner)

        response = self.client.get(self.detail_url)

        self.assertIn(campaign, response.context["created_campaigns"])
        self.assertIn(joined_campaign, response.context["participating_campaigns"])
        self.assertIn(character, response.context["created_characters"])
