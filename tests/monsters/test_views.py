from django.test import TestCase
from django.urls import reverse

from tests.helpers import create_campaign, create_campaign_monster, create_monster, create_user


class MonsterListViewTests(TestCase):
    def test_search_strips_whitespace_and_filters_by_name(self):
        match = create_monster("Cave Stalker")
        create_monster("Marsh Drake")

        response = self.client.get(reverse("monsters:monster-list"), {"name": "  cave  "})

        self.assertEqual(list(response.context["monster_list"]), [match])


class CampaignMonsterCreationViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("monster-owner")
        self.other = create_user("monster-other")
        self.campaign = create_campaign(creator=self.owner)
        self.other_campaign = create_campaign(creator=self.other, title="Other Monster Campaign")
        self.base_monster = create_monster("Ash Hound")
        self.url = reverse("campaigns:campaign-monster-list", args=[self.campaign.pk])

    def test_campaign_monster_page_is_restricted_to_owner(self):
        self.client.force_login(self.other)

        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_base_monster_route_prefills_form_values(self):
        self.client.force_login(self.owner)
        url = reverse(
            "campaigns:campaign-monster-create-from-monster",
            args=[self.campaign.pk, self.base_monster.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.context["form"]["name"].value(), self.base_monster.name)
        self.assertEqual(int(response.context["form"]["base_monster"].value()), self.base_monster.pk)

    def test_campaign_monster_creation_assigns_campaign_and_scopes_context(self):
        own_monster = create_campaign_monster(self.campaign, name="Local Beast")
        create_campaign_monster(self.other_campaign, name="Remote Beast")
        self.client.force_login(self.owner)

        response = self.client.get(self.url)
        self.assertEqual(list(response.context["campaign_monsters"]), [own_monster])

        response = self.client.post(
            self.url,
            {
                "base_monster": self.base_monster.pk,
                "name": "Campaign Ash Hound",
                "type": self.base_monster.type,
                "alignment": self.base_monster.alignment,
                "challenge_rating": self.base_monster.challenge_rating,
                "hit_points": self.base_monster.hit_points,
                "armor_class": self.base_monster.armor_class,
                "abilities": self.base_monster.abilities,
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.assertTrue(
            self.campaign.monsters.filter(
                name="Campaign Ash Hound", base_monster=self.base_monster
            ).exists()
        )
