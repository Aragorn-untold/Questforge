from django import forms

from compendium.monsters.models import CampaignMonster


class CampaignMonsterForm(forms.ModelForm):
    class Meta:
        model = CampaignMonster
        fields = (
            "base_monster",
            "name",
            "type",
            "alignment",
            "challenge_rating",
            "hit_points",
            "armor_class",
            "abilities"
        )


class MonsterSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        )
    )
