from django.test import TestCase
from django.urls import reverse

from campaigns.models import Campaign
from tests.helpers import create_campaign, create_character, create_character_class, create_race, create_user


class CharacterViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("character-owner")
        self.player = create_user("character-player")
        self.other = create_user("character-other")
        self.campaign = create_campaign(creator=self.owner)
        self.race = create_race()
        self.character_class = create_character_class()

    def test_join_assigns_campaign_and_player_from_request_context(self):
        self.client.force_login(self.player)
        url = reverse("campaigns:characters:character-create", args=[self.campaign.pk])

        response = self.client.post(
            url,
            {
                "name": "Joined Hero",
                "race": self.race.pk,
                "character_class": self.character_class.pk,
                "gender": "O",
                "bio": "Ready for an adventure.",
                "player": self.other.pk,
                "campaign": 999999,
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        character = self.campaign.characters.get()
        self.assertEqual(character.player, self.player)
        self.assertEqual(character.campaign, self.campaign)

    def test_join_attempt_redirects_if_player_already_has_a_character(self):
        create_character(self.campaign, self.player)
        self.client.force_login(self.player)

        response = self.client.get(
            reverse("campaigns:characters:character-create", args=[self.campaign.pk])
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.assertEqual(self.campaign.characters.filter(player=self.player).count(), 1)

    def test_player_cannot_join_an_ended_campaign(self):
        self.campaign.is_active = Campaign.ActiveChoice.ENDED
        self.campaign.save(update_fields=["is_active"])
        self.client.force_login(self.player)

        response = self.client.post(
            reverse("campaigns:characters:character-create", args=[self.campaign.pk]),
            {
                "name": "Too Late Hero",
                "race": self.race.pk,
                "character_class": self.character_class.pk,
                "gender": "O",
                "bio": "",
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.assertFalse(self.campaign.characters.filter(player=self.player).exists())

    def test_character_list_is_limited_to_its_campaign(self):
        listed = create_character(self.campaign, self.player, name="Listed Hero")
        other_campaign = create_campaign(creator=self.owner, title="Other Campaign")
        create_character(other_campaign, self.other, name="Hidden Hero")

        response = self.client.get(
            reverse("campaigns:characters:character-list", args=[self.campaign.pk])
        )

        self.assertEqual(list(response.context["object_list"]), [listed])

    def test_character_detail_keeps_profile_return_target(self):
        character = create_character(self.campaign, self.player)
        response = self.client.get(
            reverse(
                "campaigns:characters:character-detail",
                args=[self.campaign.pk, character.pk],
            ),
            {"from_profile": self.other.pk},
        )

        self.assertEqual(response.context["return_profile_user"], self.other)

    def test_player_cannot_update_or_delete_another_players_character(self):
        character = create_character(self.campaign, self.player)
        self.client.force_login(self.other)
        update_url = reverse(
            "campaigns:characters:character-update",
            args=[self.campaign.pk, character.pk],
        )
        delete_url = reverse(
            "campaigns:characters:character-delete",
            args=[self.campaign.pk, character.pk],
        )

        self.assertEqual(self.client.get(update_url).status_code, 404)
        self.assertEqual(self.client.get(delete_url).status_code, 404)
