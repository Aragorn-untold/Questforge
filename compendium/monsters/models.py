from django.db import models

from campaigns.models import Campaign


class Monster(models.Model):
    class ChallengeChoice(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"
        DEADLY = "DEADLY", "Deadly"

    class TypeChoice(models.TextChoices):
        ABERRATION = "ABERRATION", "Aberration"
        BEAST = "BEAST", "Beast"
        CELESTIAL = "CELESTIAL", "Celestial"
        CONSTRUCT = "CONSTRUCT", "Construct"
        DRAGON = "DRAGON", "Dragon"
        ELEMENTAL = "ELEMENTAL", "Elemental"
        FEY = "FEY", "Fey"
        FIEND = "FIEND", "Fiend"
        GIANT = "GIANT", "Giant"
        HUMANOID = "HUMANOID", "Humanoid"
        MONSTROSITY = "MONSTROSITY", "Monstrosity"
        PLANT = "PLANT", "Plant"
        UNDEAD = "UNDEAD", "Undead"

    class AlignmentChoice(models.TextChoices):
        LAWFUL_GOOD = "LAWFUL_GOOD", "Lawful Good"
        NEUTRAL_GOOD = "NEUTRAL_GOOD", "Neutral Good"
        CHAOTIC_GOOD = "CHAOTIC_GOOD", "Chaotic Good"
        LAWFUL_NEUTRAL = "LAWFUL_NEUTRAL", "Lawful Neutral"
        TRUE_NEUTRAL = "TRUE_NEUTRAL", "Neutral"
        CHAOTIC_NEUTRAL = "CHAOTIC_NEUTRAL", "Chaotic Neutral"
        LAWFUL_EVIL = "LAWFUL_EVIL", "Lawful Evil"
        NEUTRAL_EVIL = "NEUTRAL_EVIL", "Neutral Evil"
        CHAOTIC_EVIL = "CHAOTIC_EVIL", "Chaotic Evil"
        UNALIGNED = "UNALIGNED", "Unaligned"

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=33, choices=TypeChoice.choices)
    alignment = models.CharField(max_length=55, choices=AlignmentChoice.choices, default=AlignmentChoice.UNALIGNED)
    challenge_rating = models.CharField(max_length=35, choices=ChallengeChoice.choices)
    hit_points = models.IntegerField()
    armor_class = models.IntegerField()
    abilities = models.TextField() # should be a separate table

    def __str__(self) -> str:
        return f"{self.name} | {self.get_type_display()} | {self.get_challenge_rating_display()}"

    def to_campaign_monster(self):
        return {
            "base_monster": self.id,
            "name": self.name,
            "type": self.type,
            "alignment": self.alignment,
            "challenge_rating": self.challenge_rating,
            "hit_points": self.hit_points,
            "armor_class": self.armor_class,
            "abilities": self.abilities
        }

    class Meta:
        ordering = ["name"]


class CampaignMonster(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='monsters')
    base_monster = models.ForeignKey(Monster, on_delete=models.SET_NULL, null=True, blank=True, related_name='campaign_monsters')
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=33, choices=Monster.TypeChoice.choices)
    alignment = models.CharField(max_length=55, choices=Monster.AlignmentChoice.choices, default=Monster.AlignmentChoice.UNALIGNED)
    challenge_rating = models.CharField(max_length=35, choices=Monster.ChallengeChoice.choices)
    hit_points = models.IntegerField()
    armor_class = models.IntegerField()
    abilities = models.TextField() # should be a separate table

    def __str__(self) -> str:
        return f"{self.name} | {self.get_type_display()} | {self.get_challenge_rating_display()}"

    class Meta:
        ordering = ["name"]
