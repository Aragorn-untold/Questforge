from decimal import Decimal

from django.test import TestCase

from tests.helpers import create_item


class ItemCatalogConversionTests(TestCase):
    def test_to_campaign_item_copies_catalog_values(self):
        item = create_item(
            name="Moonsteel Blade",
            damage="1d8 radiant",
            price=Decimal("125.00"),
        )

        self.assertEqual(
            item.to_campaign_item(),
            {
                "base_item": item,
                "name": "Moonsteel Blade",
                "type": item.type,
                "rarity": item.rarity,
                "description": item.description,
                "damage": "1d8 radiant",
                "protection": item.protection,
                "effect": item.effect,
                "weight": item.weight,
                "price": Decimal("125.00"),
            },
        )
