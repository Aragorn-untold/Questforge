from django.db import IntegrityError, transaction
from django.test import TestCase

from tests.helpers import create_campaign, create_character, create_user


class CharacterModelConstraintTests(TestCase):
    def test_player_cannot_have_two_characters_in_one_campaign(self):
        player = create_user("one-character-player")
        campaign = create_campaign()
        create_character(campaign, player, name="First Hero")

        with self.assertRaises(IntegrityError), transaction.atomic():
            create_character(campaign, player, name="Second Hero")

    def test_same_player_can_have_characters_in_different_campaigns(self):
        player = create_user("multi-campaign-player")
        first = create_campaign(title="First Campaign")
        second = create_campaign(title="Second Campaign")

        create_character(first, player, name="First Hero")
        create_character(second, player, name="Second Hero")

        self.assertEqual(player.characters.count(), 2)
