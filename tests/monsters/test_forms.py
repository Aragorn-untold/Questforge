from django.test import SimpleTestCase

from monsters.forms import CampaignMonsterForm, MonsterSearchForm


class MonsterFormConfigurationTests(SimpleTestCase):
    def test_campaign_monster_form_cannot_choose_a_campaign(self):
        form = CampaignMonsterForm()

        self.assertNotIn("campaign", form.fields)
        self.assertIn("base_monster", form.fields)

    def test_monster_search_is_optional(self):
        self.assertTrue(MonsterSearchForm(data={}).is_valid())
