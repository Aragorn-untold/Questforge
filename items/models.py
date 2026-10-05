from django.db import models

from campaigns.models import Campaign


class Item(models.Model):
    class TypeChoice(models.TextChoices):
        WEAPON = 'WEAPON', 'Weapon'
        ARMOR = 'ARMOR', 'Armor'
        POTION = 'POTION', 'Potion'
        SCROLL = 'SCROLL', 'Scroll'
        RING = 'RING', 'Ring'
        AMULET = 'AMULET', 'Amulet'
        WAND = 'WAND', 'Wand'
        MISC = 'MISC', 'Miscellaneous'

    class RarityChoice(models.TextChoices):
        COMMON = 'COMMON', 'Common'
        UNCOMMON = 'UNCOMMON', 'Uncommon'
        RARE = 'RARE', 'Rare'
        VERY_RARE = 'VERY_RARE', 'Very Rare'
        LEGENDARY = 'LEGENDARY', 'Legendary'
        ARTIFACT = 'ARTIFACT', 'Artifact'

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=20,
        choices=TypeChoice.choices,
        default=TypeChoice.MISC,
    )
    rarity = models.CharField(
        max_length=20,
        choices=RarityChoice.choices,
        default=RarityChoice.COMMON,
    )
    description = models.TextField()
    damage = models.CharField(max_length=60, null=True, blank=True)
    protection = models.CharField(max_length=60, null=True, blank=True)
    effect = models.CharField(max_length=60, null=True, blank=True)
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def to_campaign_item(self) -> dict:
        return {
            "base_item": self,
            "name": self.name,
            "type": self.type,
            "rarity": self.rarity,
            "description": self.description,
            "damage": self.damage,
            "protection": self.protection,
            "effect": self.effect,
            "weight": self.weight,
            "price": self.price,
        }

    class Meta:
        ordering = ["name"]


class CampaignItem(models.Model):
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="items",
    )

    base_item = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="campaign_items",
    )

    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=20,
        choices=Item.TypeChoice.choices,
    )
    rarity = models.CharField(
        max_length=20,
        choices=Item.RarityChoice.choices,
    )
    description = models.TextField()
    damage = models.CharField(max_length=60, null=True, blank=True)
    protection = models.CharField(max_length=60, null=True, blank=True)
    effect = models.CharField(max_length=60, null=True, blank=True)
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
