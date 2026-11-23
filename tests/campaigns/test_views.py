from django.test import TestCase
from django.urls import reverse

from campaigns.models import Campaign, CampaignNote
from tests.helpers import create_campaign, create_character, create_user


class CampaignListViewTests(TestCase):
    def test_search_filters_campaign_titles_without_case_sensitivity(self):
        match = create_campaign(title="The Silver Dragon")
        create_campaign(title="Quiet Hamlet")

        response = self.client.get(reverse("campaigns:campaign-list"), {"title": "sIlVeR"})

        self.assertEqual(list(response.context["campaign_list"]), [match])


class CampaignOwnershipViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("campaign-owner")
        self.other = create_user("campaign-other")
        self.campaign = create_campaign(creator=self.owner)
        self.update_url = reverse("campaigns:campaign-update", args=[self.campaign.pk])
        self.delete_url = reverse("campaigns:campaign-delete", args=[self.campaign.pk])

    def test_campaign_creation_assigns_authenticated_user_as_creator(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("campaigns:campaign-create"),
            {
                "title": "Owner Assigned",
                "description": "Created in the test.",
                "creator": self.other.pk,
            },
        )

        self.assertRedirects(response, reverse("campaigns:campaign-list"))
        created = Campaign.objects.get(title="Owner Assigned")
        self.assertEqual(created.creator, self.owner)

    def test_non_owner_cannot_update_or_delete_campaign(self):
        self.client.force_login(self.other)

        self.assertEqual(self.client.get(self.update_url).status_code, 403)
        self.assertEqual(self.client.get(self.delete_url).status_code, 403)

    def test_owner_can_update_campaign_and_success_returns_to_its_detail(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.update_url,
            {
                "title": self.campaign.title,
                "description": "Updated by the owner.",
                "start_date": "2030-01-02T12:15",
                "is_active": Campaign.ActiveChoice.ACTIVE,
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.description, "Updated by the owner.")

    def test_campaign_detail_resolves_profile_return_context(self):
        response = self.client.get(
            self.campaign.get_absolute_url(), {"from_profile": self.other.pk}
        )

        self.assertEqual(response.context["return_profile_user"], self.other)


class CampaignNoteViewTests(TestCase):
    def setUp(self):
        self.game_master = create_user("notes-game-master")
        self.player = create_user("notes-player")
        self.campaign = create_campaign(creator=self.game_master, title="Notes Campaign")
        create_character(self.campaign, self.player, name="Notes Player Hero")
        self.note = CampaignNote.objects.create(
            campaign=self.campaign,
            user=self.game_master,
            content="A private clue for the game master.",
        )
        self.create_url = reverse(
            "campaigns:campaign-note-create", args=[self.campaign.pk]
        )
        self.update_url = reverse(
            "campaigns:campaign-note-update", args=[self.campaign.pk, self.note.pk]
        )
        self.delete_url = reverse(
            "campaigns:campaign-note-delete", args=[self.campaign.pk, self.note.pk]
        )

    def test_only_game_master_sees_the_campaign_notes_section(self):
        self.client.force_login(self.game_master)
        response = self.client.get(self.campaign.get_absolute_url())

        self.assertContains(response, 'id="campaign-notes"')
        self.assertContains(response, self.note.content)

        self.client.force_login(self.player)
        response = self.client.get(self.campaign.get_absolute_url())

        self.assertNotContains(response, 'id="campaign-notes"')
        self.assertNotContains(response, self.note.content)

        self.client.logout()
        response = self.client.get(self.campaign.get_absolute_url())

        self.assertNotContains(response, 'id="campaign-notes"')
        self.assertNotContains(response, self.note.content)

    def test_game_master_can_create_and_edit_campaign_notes(self):
        self.client.force_login(self.game_master)

        response = self.client.post(self.create_url, {"content": "A fresh clue."})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"], f"{self.campaign.get_absolute_url()}#campaign-notes"
        )
        created_note = CampaignNote.objects.get(content="A fresh clue.")
        self.assertEqual(created_note.user, self.game_master)
        self.assertEqual(created_note.campaign, self.campaign)

        response = self.client.post(self.update_url, {"content": "Updated clue."})

        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, "Updated clue.")

    def test_non_game_master_cannot_create_edit_or_delete_notes(self):
        self.client.force_login(self.player)

        self.assertEqual(
            self.client.post(self.create_url, {"content": "Should not be saved."}).status_code,
            403,
        )
        self.assertEqual(self.client.get(self.update_url).status_code, 403)
        self.assertEqual(self.client.get(self.delete_url).status_code, 403)

    def test_game_master_can_delete_a_note(self):
        self.client.force_login(self.game_master)

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(CampaignNote.objects.filter(pk=self.note.pk).exists())
