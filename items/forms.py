from django import forms

from items.models import CampaignItem


class CampaignItemForm(forms.ModelForm):
    class Meta:
        model = CampaignItem
        fields = [
            "base_item",
            "name",
            "type",
            "rarity",
            "description",
            "damage",
            "protection",
            "effect",
            "weight",
            "price",
        ]


class ItemSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )
