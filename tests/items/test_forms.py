from django.test import SimpleTestCase

from items.forms import CampaignItemForm, ItemSearchForm


class ItemFormConfigurationTests(SimpleTestCase):
    def test_campaign_item_form_cannot_choose_a_campaign(self):
        form = CampaignItemForm()

        self.assertNotIn("campaign", form.fields)
        self.assertIn("base_item", form.fields)

    def test_item_search_is_optional(self):
        self.assertTrue(ItemSearchForm(data={}).is_valid())
