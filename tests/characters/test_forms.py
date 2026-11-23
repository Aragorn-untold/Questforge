from django.test import SimpleTestCase

from characters.views import CharacterCreateView


class CharacterCreationFormConfigurationTests(SimpleTestCase):
    def test_player_and_campaign_are_not_client_editable_fields(self):
        form = CharacterCreateView().get_form_class()()

        self.assertNotIn("player", form.fields)
        self.assertNotIn("campaign", form.fields)
        self.assertIn("race", form.fields)
        self.assertIn("character_class", form.fields)
