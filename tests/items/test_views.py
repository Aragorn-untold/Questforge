from django.test import TestCase
from django.urls import reverse

from tests.helpers import create_campaign, create_campaign_item, create_item, create_user


class ItemListViewTests(TestCase):
    def test_search_filters_catalog_items_by_name(self):
        match = create_item("Silvered Dagger")
        create_item("Oak Shield")

        response = self.client.get(reverse("compendium:items:item-list"), {"name": "SILVER"})

        self.assertEqual(list(response.context["item_list"]), [match])


class CampaignItemCreationViewTests(TestCase):
    def setUp(self):
        self.owner = create_user("item-owner")
        self.other = create_user("item-other")
        self.campaign = create_campaign(creator=self.owner)
        self.other_campaign = create_campaign(creator=self.other, title="Other Item Campaign")
        self.base_item = create_item("Healing Draught")
        self.url = reverse("campaigns:campaign-item-list", args=[self.campaign.pk])

    def test_campaign_item_page_is_restricted_to_owner(self):
        self.client.force_login(self.other)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_base_item_route_prefills_form_values(self):
        self.client.force_login(self.owner)
        url = reverse(
            "campaigns:campaign-item-create-from-item",
            args=[self.campaign.pk, self.base_item.pk],
        )

        response = self.client.get(url)

        self.assertEqual(response.context["form"]["name"].value(), self.base_item.name)
        self.assertEqual(int(response.context["form"]["base_item"].value()), self.base_item.pk)

    def test_create_assigns_campaign_and_lists_only_its_items(self):
        own_item = create_campaign_item(self.campaign, name="Only Here")
        create_campaign_item(self.other_campaign, name="Over There")
        self.client.force_login(self.owner)

        response = self.client.get(self.url)

        self.assertEqual(list(response.context["campaign_items"]), [own_item])

        response = self.client.post(
            self.url,
            {
                "base_item": self.base_item.pk,
                "name": "Campaign Healing Draught",
                "type": self.base_item.type,
                "rarity": self.base_item.rarity,
                "description": self.base_item.description,
                "damage": self.base_item.damage or "",
                "protection": self.base_item.protection or "",
                "effect": self.base_item.effect or "",
                "weight": self.base_item.weight,
                "price": self.base_item.price,
            },
        )

        self.assertRedirects(response, self.campaign.get_absolute_url())
        self.assertTrue(
            self.campaign.items.filter(
                name="Campaign Healing Draught", base_item=self.base_item
            ).exists()
        )
