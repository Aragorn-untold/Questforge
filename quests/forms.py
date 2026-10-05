from django import forms

from quests.models import CampaignQuest


class CampaignQuestForm(forms.ModelForm):
    class Meta:
        model = CampaignQuest
        fields = (
            "base_quest",
            "title",
            "description",
            "reward_description",
            "difficulty_rating",
            "level_recommendation"
        )


class QuestSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by title"}
        )
    )
