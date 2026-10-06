from django.test import TestCase
from django.utils import timezone

from campaigns.forms import CampaignNoteForm, CampaignSearchForm, CampaignUpdateForm
from campaigns.models import Campaign
from tests.helpers import create_campaign


class CampaignUpdateFormTests(TestCase):
    def test_start_date_uses_datetime_local_widget_and_local_initial(self):
        form = CampaignUpdateForm()

        self.assertEqual(form.fields["start_date"].widget.input_type, "datetime-local")
        self.assertEqual(form.fields["start_date"].input_formats, ["%Y-%m-%dT%H:%M"])
        self.assertIsNotNone(form["start_date"].value())

    def test_blank_start_date_is_allowed(self):
        campaign = create_campaign()
        form = CampaignUpdateForm(
            data={
                "title": campaign.title,
                "description": campaign.description,
                "start_date": "",
                "is_active": Campaign.ActiveChoice.ACTIVE,
            },
            instance=campaign,
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertIsNone(form.cleaned_data["start_date"])

    def test_custom_datetime_format_parses_as_an_aware_datetime(self):
        campaign = create_campaign()
        form = CampaignUpdateForm(
            data={
                "title": campaign.title,
                "description": campaign.description,
                "start_date": "2031-05-04T18:30",
                "is_active": Campaign.ActiveChoice.PAUSED,
            },
            instance=campaign,
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["start_date"].minute, 30)
        self.assertTrue(timezone.is_aware(form.cleaned_data["start_date"]))


class CampaignSearchFormTests(TestCase):
    def test_search_term_is_optional(self):
        self.assertTrue(CampaignSearchForm(data={}).is_valid())


class CampaignNoteFormTests(TestCase):
    def test_only_note_content_is_editable(self):
        form = CampaignNoteForm()

        self.assertEqual(tuple(form.fields), ("content",))
        self.assertEqual(form.fields["content"].widget.attrs["rows"], 5)
        self.assertIn("class", form.fields["content"].widget.attrs)
