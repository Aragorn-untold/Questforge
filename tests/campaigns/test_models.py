from django.test import TestCase
from django.urls import reverse

from campaigns.models import CampaignNote
from tests.helpers import create_campaign, create_user


class CampaignModelTests(TestCase):
    def test_campaign_url_and_string_representation(self):
        campaign = create_campaign(title="The Amber Road")

        self.assertEqual(campaign.get_absolute_url(), reverse("campaigns:campaign-detail", args=[campaign.pk]))
        self.assertEqual(str(campaign), "The Amber Road")


class CampaignNoteModelTests(TestCase):
    def test_campaign_and_user_reverse_relations_use_note_names(self):
        campaign = create_campaign()
        user = create_user("note-author")
        note = CampaignNote.objects.create(
            campaign=campaign,
            user=user,
            content="The old bridge is watched.",
        )

        self.assertEqual(campaign.notes.get(), note)
        self.assertEqual(user.campaign_notes.get(), note)
