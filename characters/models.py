from django.contrib.auth import get_user_model
from django.db import models

from campaigns.models import Campaign
from compendium.items.models import CampaignItem


class Character(models.Model):
    class GenderChoice(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="characters"
    )
    player = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="characters"
    )
    name = models.CharField(max_length=120)
    level = models.IntegerField(default=1)
    experience = models.FloatField(default=0.0)
    gender = models.CharField(
        max_length=30, choices=GenderChoice, default=GenderChoice.OTHER
    )
    bio = models.TextField(blank=True)
    race = models.ForeignKey(
        "Race", on_delete=models.CASCADE, related_name="characters"
    )
    character_class = models.ForeignKey(
        "CharacterClass", on_delete=models.CASCADE, related_name="characters"
    )
    items = models.ManyToManyField(
        CampaignItem,
        blank=True,
        related_name="characters",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("campaign", "player"),
                name="unique_character_per_player_per_campaign",
            )
        ]


class Race(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ability = models.CharField(max_length=255)  # Create a separate table for it?
    race_traits_description = models.TextField()  # Also a separate table?

    def __str__(self) -> str:
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ability = models.CharField(max_length=255)
    class_traits_description = models.TextField()
    # proficiencies =
    # subclasses_description =

    def __str__(self) -> str:
        return self.name
