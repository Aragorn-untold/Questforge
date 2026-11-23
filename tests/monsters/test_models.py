from django.test import TestCase

from tests.helpers import create_monster


class MonsterCatalogConversionTests(TestCase):
    def test_to_campaign_monster_copies_stats_and_catalog_reference(self):
        monster = create_monster("Cave Stalker", hit_points=42, armor_class=15)

        self.assertEqual(
            monster.to_campaign_monster(),
            {
                "base_monster": monster.pk,
                "name": monster.name,
                "type": monster.type,
                "alignment": monster.alignment,
                "challenge_rating": monster.challenge_rating,
                "hit_points": 42,
                "armor_class": 15,
                "abilities": monster.abilities,
            },
        )

    def test_string_representation_includes_type_and_challenge_rating(self):
        monster = create_monster("Cave Stalker")

        self.assertEqual(str(monster), "Cave Stalker | Beast | Easy")
