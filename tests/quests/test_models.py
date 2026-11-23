from django.test import TestCase

from tests.helpers import create_quest


class QuestCatalogConversionTests(TestCase):
    def test_to_campaign_quest_copies_all_editable_catalog_values(self):
        quest = create_quest(title="The Glass Tower")

        self.assertEqual(
            quest.to_campaign_quest(),
            {
                "title": quest.title,
                "description": quest.description,
                "reward_description": quest.reward_description,
                "difficulty_rating": quest.difficulty_rating,
                "level_recommendation": quest.level_recommendation,
            },
        )
