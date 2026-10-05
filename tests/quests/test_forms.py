from django.test import SimpleTestCase

from quests.forms import CampaignQuestForm, QuestSearchForm


class QuestFormConfigurationTests(SimpleTestCase):
    def test_campaign_quest_form_cannot_choose_a_campaign(self):
        form = CampaignQuestForm()

        self.assertNotIn("campaign", form.fields)
        self.assertIn("base_quest", form.fields)

    def test_quest_search_is_optional(self):
        self.assertTrue(QuestSearchForm(data={}).is_valid())
