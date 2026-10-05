from django import forms
from django.utils import timezone

from campaigns.models import Campaign, CampaignNote


class CampaignNoteForm(forms.ModelForm):
    class Meta:
        model = CampaignNote
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write down an important moment, party decision, or clue…",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["content"].widget.attrs["class"] = "form-control campaign-note-input"


class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ("title", "description", "start_date", "is_active")
        widgets = {
            "start_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        start_date = self.fields["start_date"]
        start_date.required = False
        start_date.input_formats = ["%Y-%m-%dT%H:%M"]
        start_date.help_text = "Choose the campaign start date and time."

        if not self.is_bound and not self.instance.start_date:
            start_date.initial = timezone.localtime().replace(second=0, microsecond=0)


class CampaignSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by title"}
        )
    )
