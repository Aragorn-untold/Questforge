from django.test import TestCase
from django.urls import reverse

from tests.helpers import create_campaign, create_campaign_quest, create_quest, create_user


class QuestListViewTests(TestCase):
    def test_search_filters_quests_by_title(self):
        match = create_quest("The Lost Crown")
        create_quest("A Quiet Crossing")

        response = self.client.get(reverse("quests:quest-list"), {"title": "lost"})

        self.assertEqual(list(response.context["quest_list"]), [match])


class CampaignQuestCreationViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("quest-owner")
        self.other = create_user("quest-other")
        self.campaign = create_campaign(creator=self.owner)
        self.other_campaign = create_campaign(creator=self.other, title="Other Quest Campaign")
        self.base_quest = create_quest("The Buried Bell")
        self.url = reverse("campaigns:campaign-quest-list", args=[self.campaign.pk])

    def test_campaign_quest_page_is_restricted_to_owner(self):
        self.client.force_login(self.other)

        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_base_quest_route_prefills_form_values(self):
        self.client.force_login(self.owner)
        url = reverse(
            "campaigns:campaign-quest-create-from-item",
            args=[self.campaign.pk, self.base_quest.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.context["form"]["title"].value(), self.base_quest.title)

    def test_campaign_quest_creation_assigns_campaign_and_scopes_context(self):
        own_quest = create_campaign_quest(self.campaign, title="Local Quest")
        create_campaign_quest(self.other_campaign, title="Remote Quest")
        self.client.force_login(self.owner)

        response = self.client.get(self.url)
        self.assertEqual(list(response.context["campaign_quests"]), [own_quest])

        response = self.client.post(
            self.url,
            {
                "base_quest": self.base_quest.pk,
                "title": "Campaign Buried Bell",
                "description": self.base_quest.description,
                "reward_description": self.base_quest.reward_description,
                "difficulty_rating": self.base_quest.difficulty_rating,
                "level_recommendation": self.base_quest.level_recommendation,
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.assertTrue(
            self.campaign.quests.filter(
                title="Campaign Buried Bell", base_quest=self.base_quest
            ).exists()
        )
